from __future__ import annotations
import json
import math
import sys
import statistics
from pathlib import Path
from typing import Dict, List, Tuple, Any

# ---------- OpenCascade ----------
from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.IFSelect    import IFSelect_RetDone, IFSelect_ReturnStatus
from OCC.Core.TopAbs      import TopAbs_FACE, TopAbs_EDGE, TopAbs_WIRE, TopAbs_VERTEX
from OCC.Core.TopExp      import TopExp_Explorer
from OCC.Core.BRep        import BRep_Tool
from OCC.Core.BRepTools   import breptools
from OCC.Core.BRepBndLib  import brepbndlib # For static Add and AddOBB
from OCC.Core.BRepGProp   import brepgprop
from OCC.Core.Bnd         import Bnd_Box, Bnd_OBB
from OCC.Core.GProp       import GProp_GProps
# from OCC.Core.Geom        import Geom_Surface # Not directly used for IsNull
from OCC.Core.GeomAdaptor import GeomAdaptor_Surface, GeomAdaptor_Curve
from OCC.Core.GeomAbs     import (
    GeomAbs_Plane, GeomAbs_Cylinder, GeomAbs_BSplineSurface,
    GeomAbs_SurfaceOfRevolution, GeomAbs_Line, GeomAbs_Circle,
    GeomAbs_BSplineCurve, GeomAbs_Cone, GeomAbs_Sphere, GeomAbs_Torus
)
from OCC.Core.GeomLProp   import GeomLProp_SLProps
# Import TopoDS specific types for type hinting and for casting via their .Cast() static method
from OCC.Core.TopoDS import TopoDS_Shape, TopoDS_Face, TopoDS_Edge, TopoDS_Wire, TopoDS_Vertex, topods
from OCC.Core.gp          import gp_Pnt, gp_Dir # For point and direction types if needed explicitly

class StepParser:
    """
    Parses a STEP file to extract geometric and topological information.
    """
    def __init__(self, step_path: Path):
        self.step_path = step_path.expanduser().resolve()
        if not self.step_path.exists() or not self.step_path.is_file():
            raise FileNotFoundError(f"STEP file not found or is not a file: {self.step_path}")
        
        self.shape: TopoDS_Shape | None = self._load_step()
        if self.shape is None or self.shape.IsNull():
             raise RuntimeError(f"Failed to load a valid shape from STEP file: {self.step_path} or main shape is Null.")
        
        self._processed_edges_map: Dict[int, str] = {}
        self._wire_to_id_map: Dict[int, str] = {}

    def _load_step(self) -> TopoDS_Shape | None:
        reader = STEPControl_Reader()
        status = reader.ReadFile(str(self.step_path))
        if status != IFSelect_ReturnStatus.IFSelect_RetDone:
            error_map = {
                IFSelect_ReturnStatus.IFSelect_RetFail: "General failure",
                IFSelect_ReturnStatus.IFSelect_RetError: "Error in command",
                IFSelect_ReturnStatus.IFSelect_RetVoid: "Void result, no data",
                IFSelect_ReturnStatus.IFSelect_RetStop: "Stopped by user",
            }
            status_msg = error_map.get(status, f"Unknown status code: {status}")
            raise RuntimeError(f"STEP read failed for {self.step_path}. Status: {status_msg}")
        
        num_roots_transferred = reader.TransferRoots()
        if num_roots_transferred == 0:
            # print(f"Warning: No roots transferred from STEP file {self.step_path}.", file=sys.stderr)
            return None
        
        if reader.NbShapes() > 0:
            shape = reader.OneShape()
            if shape is not None and not shape.IsNull():
                return shape
            else:
                # print(f"Warning: Transferred shape from {self.step_path} is Null or invalid.", file=sys.stderr)
                return None
        else:
            # print(f"Warning: No shapes found in STEP file {self.step_path} after transfer.", file=sys.stderr)
            return None

    def _get_safe_hashcode(self, shape_obj: TopoDS_Shape, default_value: int = -1, upper_bound: int = 20000000) -> int:
        if shape_obj is None or shape_obj.IsNull():
            return default_value
        try:
            if hasattr(shape_obj, 'HashCode') and callable(getattr(shape_obj, 'HashCode')):
                return shape_obj.HashCode(upper_bound)
        except Exception as e_hash: # Catch any exception during HashCode call
            print(f"Warning: Exception while getting HashCode for {type(shape_obj)}. Error: {e_hash}", file=sys.stderr)
            # pass # Continue, returning default_value
        return default_value

    def _get_shape_bbox(self, shape_to_bound: TopoDS_Shape, oriented: bool = False) -> Dict[str, List[float]] | None:
        if shape_to_bound is None or shape_to_bound.IsNull():
            return None
        try:
            if oriented:
                obb = Bnd_OBB()
                brepbndlib.AddOBB(shape_to_bound, obb, True, True)
                if obb.IsVoid(): return None
                c = obb.Center()
                return dict(
                    center=[round(c.X(), 6), round(c.Y(), 6), round(c.Z(), 6)],
                    half_size=[round(obb.XHSize(), 6), round(obb.YHSize(), 6), round(obb.ZHSize(), 6)]
                )
            else:
                box = Bnd_Box()
                brepbndlib.Add(shape_to_bound, box)
                if box.IsVoid(): return None
                xmin, ymin, zmin, xmax, ymax, zmax = box.Get()
                return dict(
                    min=[round(xmin, 6), round(ymin, 6), round(zmin, 6)],
                    max=[round(xmax, 6), round(ymax, 6), round(zmax, 6)]
                )
        except Exception as e:
            print(f"Warning: Exception in _get_shape_bbox for {type(shape_to_bound)}. Error: {e}", file=sys.stderr)
            return None

    def _get_curvature_stats(self, surf_adapt: GeomAdaptor_Surface, umin: float, umax: float, vmin: float, vmax: float,
                           n_samples: int = 5) -> Tuple[float, float]:
        h_vals, k_vals = [], []
        if abs(umax - umin) < 1e-9 or abs(vmax - vmin) < 1e-9:
            return 0.0, 0.0
        
        the_geom_surface = surf_adapt.Surface() # Geom_Surface

        for i in range(n_samples):
            for j in range(n_samples):
                u = umin + (umax - umin) * (i + 0.5) / n_samples
                v = vmin + (vmax - vmin) * (j + 0.5) / n_samples
                try:
                    props = GeomLProp_SLProps(the_geom_surface, u, v, 2, 1e-9) 
                    if props.IsCurvatureDefined():
                        h_vals.append(abs(props.MeanCurvature()))
                        k_vals.append(abs(props.GaussianCurvature()))
                except RuntimeError as e_curve:
                    print(f"Warning: RuntimeError in _get_curvature_stats for u={u}, v={v}. Error: {e_curve}", file=sys.stderr)
                    continue 
        if not h_vals: return 0.0, 0.0
        return round(statistics.mean(h_vals), 6), round(statistics.mean(k_vals), 6)

    def _get_nurbs_meta(self, bs_adaptor: GeomAdaptor_Surface) -> Dict[str, Any] | None:
        if bs_adaptor is None or bs_adaptor.GetType() != GeomAbs_BSplineSurface:
            return None
        
        surf = bs_adaptor.BSpline() # Geom_BSplineSurface
        
        if not surf:
            print(f"Warning: BSpline surface from adaptor is null in _get_nurbs_meta.", file=sys.stderr)
            return None

        num_u_poles, num_v_poles = 0, 0
        try:
            if hasattr(surf, 'NbUPoles') and callable(getattr(surf, 'NbUPoles')):
                num_u_poles = surf.NbUPoles()
            if hasattr(surf, 'NbVPoles') and callable(getattr(surf, 'NbVPoles')):
                num_v_poles = surf.NbVPoles()
        except Exception as e_poles: # Catch error getting pole counts
            print(f"Warning: Error getting pole counts for BSplineSurface. Error: {e_poles}", file=sys.stderr)
            # pass

        knots_u_arr, knots_v_arr = surf.UKnots(), surf.VKnots()
        knots_u = [round(knots_u_arr.Value(i), 6) for i in range(knots_u_arr.Lower(), knots_u_arr.Upper() + 1)]
        knots_v = [round(knots_v_arr.Value(i), 6) for i in range(knots_v_arr.Lower(), knots_v_arr.Upper() + 1)]
        
        return dict(
            degree=[surf.UDegree(), surf.VDegree()],
            knot_counts=[len(knots_u), len(knots_v)],
            ctrlpts_count=num_u_poles * num_v_poles,
            rational=bs_adaptor.IsURational(),
        )

    def _get_face_info(self, face_shape: TopoDS_Face, f_idx: int, oriented_bbox: bool = False) -> Tuple[Dict[str, Any] | None, List[TopoDS_Wire]]:
        wires_on_face: List[TopoDS_Wire] = []
        # face_shape (TopoDS_Face) IsNull check is done by the caller (extract_all_data)

        surf_handle = BRep_Tool.Surface(face_shape) # Handle_Geom_Surface
        
        if not surf_handle: 
            return {"id": f"face_{f_idx}", "type": "unknown_no_surface_handle", "error": "Null surface handle"}, wires_on_face

        adaptor = GeomAdaptor_Surface(surf_handle)
        geom_kind = adaptor.GetType()
        type_map = {
            GeomAbs_Plane: "plane", GeomAbs_Cylinder: "cylinder", GeomAbs_Cone: "cone",
            GeomAbs_Sphere: "sphere", GeomAbs_Torus: "torus",
            GeomAbs_SurfaceOfRevolution: "revolution", GeomAbs_BSplineSurface: "nurbs",
        }
        geom_type_str = type_map.get(geom_kind, f"other_geom_{geom_kind}")

        area = 0.0
        gprop = GProp_GProps()
        try:
            brepgprop.SurfaceProperties(face_shape, gprop)
            area = round(gprop.Mass(), 6) if gprop.Mass() > 1e-9 else 0.0
        except RuntimeError as e_gprop_surf:
            print(f"Warning: RuntimeError getting surface properties for face {f_idx}. Error: {e_gprop_surf}", file=sys.stderr)
            # pass

        umin, umax, vmin, vmax = breptools.UVBounds(face_shape)
        u0, v0 = (umin + umax) * 0.5, (vmin + vmax) * 0.5
        
        normal_vec = [0.0, 0.0, 0.0]
        try:
            props_ctr = GeomLProp_SLProps(surf_handle, u0, v0, 1, 1e-9) 
            if props_ctr.IsNormalDefined():
                n_dir = props_ctr.Normal()
                normal_vec = [round(n_dir.X(), 6), round(n_dir.Y(), 6), round(n_dir.Z(), 6)]
        except RuntimeError as e_slprops:
            print(f"Warning: RuntimeError getting normal for face {f_idx}. Error: {e_slprops}", file=sys.stderr)
            # pass

        h_mean, k_mean = self._get_curvature_stats(adaptor, umin, umax, vmin, vmax)
        
        face_data: Dict[str, Any] = {
            "id": f"face_{f_idx}", "type": geom_type_str, "area": area,
            "uv_bounds": [round(umin, 6), round(umax, 6), round(vmin, 6), round(vmax, 6)],
            "normal": normal_vec, "curvature": {"mean": h_mean, "gauss": k_mean},
            "bbox": self._get_shape_bbox(face_shape, oriented=False),
        }
        if oriented_bbox:
            face_data["obb"] = self._get_shape_bbox(face_shape, oriented=True)

        if geom_kind == GeomAbs_Plane:
            pln = adaptor.Plane()
            face_data.update(plane_origin=[round(v, 6) for v in pln.Location().Coord()],
                             plane_normal=[round(v, 6) for v in pln.Axis().Direction().Coord()])
        elif geom_kind == GeomAbs_Cylinder:
            cyl = adaptor.Cylinder()
            face_data.update(radius=round(cyl.Radius(), 6),
                             axis_location=[round(v, 6) for v in cyl.Location().Coord()],
                             axis_direction=[round(v, 6) for v in cyl.Axis().Direction().Coord()])
        elif geom_kind == GeomAbs_BSplineSurface:
            nurbs_params = self._get_nurbs_meta(adaptor)
            if nurbs_params: face_data["nurbs"] = nurbs_params
        
        wire_explorer = TopExp_Explorer(face_shape, TopAbs_WIRE)
        while wire_explorer.More():
            try:
                # Use TopoDS.Wire_() for downcasting
                current_wire = topods.Wire(wire_explorer.Current())
                if not current_wire.IsNull():
                    wires_on_face.append(current_wire)
            except RuntimeError as e_cast_wire: # If casting fails
                print(f"Warning: Shape from wire explorer for face {f_idx} is not a TopoDS_Wire. Error: {e_cast_wire}. Skipping.", file=sys.stderr)
                # pass
            wire_explorer.Next()
        
        if wires_on_face:
            face_data["outer_wire_id"] = f"wire_{f_idx}_0"
            face_data["inner_wire_ids"] = [f"wire_{f_idx}_{i}" for i in range(1, len(wires_on_face))]
        else:
            face_data["outer_wire_id"] = None
            face_data["inner_wire_ids"] = []
            
        return face_data, wires_on_face

    def _get_edge_info(self, edge_shape: TopoDS_Edge, e_idx: int, oriented_bbox: bool = False) -> Dict[str, Any] | None:
        # edge_shape (TopoDS_Edge) IsNull check is done by the caller

        edge_data: Dict[str, Any] = {
            "id": f"edge_{e_idx}", 
            "bbox": self._get_shape_bbox(edge_shape, oriented=False),
            "type": "unknown", "length": 0.0
        }
        if oriented_bbox:
            edge_data["obb"] = self._get_shape_bbox(edge_shape, oriented=True)

        length = 0.0
        try:
            gprop_edge = GProp_GProps()
            brepgprop.LinearProperties(edge_shape, gprop_edge)
            length = round(gprop_edge.Mass(), 6) if gprop_edge.Mass() > 1e-9 else 0.0
        except RuntimeError as e_gprop_edge:
            print(f"Warning: RuntimeError getting linear properties for edge {e_idx}. Error: {e_gprop_edge}", file=sys.stderr)
            # pass
        edge_data["length"] = length
        
        curve_tool_output = BRep_Tool.Curve(edge_shape)
        
        curve_handle = None
        first_param = 0.0
        last_param = 0.0
        is_degenerated_curve = False

        if isinstance(curve_tool_output, tuple) and len(curve_tool_output) == 3:
            curve_handle, first_param, last_param = curve_tool_output
            if curve_handle is None:
                is_degenerated_curve = True
            elif hasattr(curve_handle, 'IsNull') and callable(getattr(curve_handle, 'IsNull')):
                if curve_handle.IsNull():
                    is_degenerated_curve = True
            # If curve_handle is a direct Geom_Curve object (which lacks IsNull),
            # its existence implies it's a valid curve, so is_degenerated_curve remains False.
        else:
            # If BRep_Tool.Curve doesn't return 3 values, treat as degenerated
            is_degenerated_curve = True
            print(f"Warning: BRep_Tool.Curve for edge {e_idx} did not return 3 values. Output: {curve_tool_output}", file=sys.stderr)

        if is_degenerated_curve:
            edge_data["type"] = "degenerated_no_curve"
            vertex_explorer = TopExp_Explorer(edge_shape, TopAbs_VERTEX)
            if vertex_explorer.More():
                try:
                    vtx = topods.Vertex(vertex_explorer.Current()) # Cast to TopoDS_Vertex
                    if not vtx.IsNull():
                        pt = BRep_Tool.Pnt(vtx)
                        edge_data["point"] = [round(pt.X(), 6), round(pt.Y(), 6), round(pt.Z(), 6)]
                except RuntimeError as e_cast_vtx: # Casting failed
                    print(f"Warning: Failed to cast to TopoDS_Vertex for degenerated edge {e_idx}. Error: {e_cast_vtx}", file=sys.stderr)
                    # pass 
            return edge_data

        adaptor = GeomAdaptor_Curve(curve_handle, first_param, last_param)
        geom_kind = adaptor.GetType()
        
        if geom_kind == GeomAbs_Line:
            p1_gp, p2_gp = adaptor.Value(first_param), adaptor.Value(last_param)
            edge_data.update(type="line",
                             p1=[round(v, 6) for v in p1_gp.Coord()],
                             p2=[round(v, 6) for v in p2_gp.Coord()])
        elif geom_kind == GeomAbs_Circle:
            circ = adaptor.Circle()
            edge_data.update(type="circle",
                             center=[round(v, 6) for v in circ.Location().Coord()],
                             radius=round(circ.Radius(), 6),
                             normal=[round(v, 6) for v in circ.Axis().Direction().Coord()])
        elif geom_kind == GeomAbs_BSplineCurve:
            edge_data.update(type="bspline_curve")
        else:
            edge_data["type"] = f"other_geom_{geom_kind}"
        return edge_data

    def extract_all_data(self, oriented_bbox: bool = False) -> Dict[str, List[Dict[str, Any]]]:
        if self.shape is None or self.shape.IsNull():
            # print("Error: Main shape is not loaded or is null. Cannot extract data.", file=sys.stderr)
            return {"surfaces": [], "edges": [], "holes": []}

        self._processed_edges_map.clear()
        self._wire_to_id_map.clear()

        all_faces_data: List[Dict[str, Any]] = []
        all_holes_data: List[Dict[str, Any]] = []
        
        face_idx_counter = 0
        face_explorer = TopExp_Explorer(self.shape, TopAbs_FACE)
        while face_explorer.More():
            current_shape_from_explorer = face_explorer.Current()
            try:
                current_face_shape = topods.Face(current_shape_from_explorer) # Cast
            except RuntimeError as e_cast_face:
                print(f"Warning: Shape from face explorer (idx {face_idx_counter}) is not a TopoDS_Face. Error: {e_cast_face}. Skipping.", file=sys.stderr)
                face_explorer.Next()
                continue
                
            if current_face_shape.IsNull():
                face_explorer.Next()
                continue
            
            face_data_dict, wires_on_face = self._get_face_info(current_face_shape, face_idx_counter, oriented_bbox)
            
            if face_data_dict:
                all_faces_data.append(face_data_dict)
                for i, wire_shape_topo in enumerate(wires_on_face): # wire_shape_topo is TopoDS_Wire
                    # IsNull for wire_shape_topo is checked when it's added to wires_on_face
                    wire_id_str = f"wire_{face_idx_counter}_{i}"
                    wire_hash = self._get_safe_hashcode(wire_shape_topo)
                    
                    if wire_hash != -1:
                        self._wire_to_id_map[wire_hash] = wire_id_str

                    if i > 0 and face_data_dict.get("id"): # Inner wires define holes
                        all_holes_data.append({
                            "hole_id": wire_id_str,
                            "parent_face_id": face_data_dict["id"],
                            "edge_ids": []
                        })
            
            face_idx_counter += 1
            face_explorer.Next()
        
        all_edges_data: List[Dict[str, Any]] = []
        edge_idx_counter = 0
        edge_explorer = TopExp_Explorer(self.shape, TopAbs_EDGE)
        while edge_explorer.More():
            current_shape_from_explorer = edge_explorer.Current()
            try:
                current_edge_shape = topods.Edge(current_shape_from_explorer) # Cast
            except RuntimeError as e_cast_edge:
                print(f"Warning: Shape from edge explorer (idx {edge_idx_counter}) is not a TopoDS_Edge. Error: {e_cast_edge}. Skipping.", file=sys.stderr)
                edge_explorer.Next()
                continue

            if current_edge_shape.IsNull():
                edge_explorer.Next()
                continue
            
            actual_edge_id_str: str | None = None
            edge_hash = self._get_safe_hashcode(current_edge_shape)

            if edge_hash != -1 and edge_hash in self._processed_edges_map:
                actual_edge_id_str = self._processed_edges_map[edge_hash]
            else:
                edge_data_dict = self._get_edge_info(current_edge_shape, edge_idx_counter, oriented_bbox)
                if edge_data_dict:
                    all_edges_data.append(edge_data_dict)
                    actual_edge_id_str = edge_data_dict["id"]
                    if edge_hash != -1:
                        self._processed_edges_map[edge_hash] = actual_edge_id_str
                    edge_idx_counter += 1
            
            if actual_edge_id_str:
                parent_wire_explorer = TopExp_Explorer(current_edge_shape, TopAbs_WIRE)
                while parent_wire_explorer.More():
                    current_parent_wire_shape = parent_wire_explorer.Current()
                    try:
                        parent_wire_shape = topods.Wire(current_parent_wire_shape) # Cast
                    except RuntimeError as e_cast_parent_wire:
                        print(f"Warning: Shape from parent wire explorer for edge {actual_edge_id_str} is not a TopoDS_Wire. Error: {e_cast_parent_wire}. Skipping.", file=sys.stderr)
                        parent_wire_explorer.Next()
                        continue

                    if parent_wire_shape.IsNull():
                        parent_wire_explorer.Next()
                        continue
                    
                    parent_wire_hash = self._get_safe_hashcode(parent_wire_shape)
                    if parent_wire_hash != -1:
                        mapped_wire_id = self._wire_to_id_map.get(parent_wire_hash)
                        if mapped_wire_id:
                            for hole_entry in all_holes_data:
                                if hole_entry["hole_id"] == mapped_wire_id:
                                    if actual_edge_id_str not in hole_entry["edge_ids"]:
                                        hole_entry["edge_ids"].append(actual_edge_id_str)
                                    break 
                    parent_wire_explorer.Next()
            edge_explorer.Next()
            
        return {"surfaces": all_faces_data, "edges": all_edges_data, "holes": all_holes_data}

# ---------- CLI (Optional) ------------------
def main_cli():
    # ... (CLI part remains the same as previous full code version) ...
    if len(sys.argv) < 2 or sys.argv[1] in ['-h', '--help', '--version']:
        if '--version' in sys.argv:
            try:
                from OCC.Core import VERSION_STRING_EXTENDED
                print(f"pythonocc-core version: {VERSION_STRING_EXTENDED}")
            except ImportError:
                print("pythonocc-core not found or version information unavailable.")
            sys.exit(0)
            
        print(f"Usage: python {Path(__file__).name} <STEP_FILE_PATH> [--obb]")
        print("\nExtracts geometry data from a STEP file to a JSON file.")
        print("Options:")
        print("  --obb       Additionally calculate Oriented Bounding Boxes (OBB).")
        print("  --version   Display pythonocc-core version and exit.")
        print("  -h, --help  Display this help message and exit.")
        sys.exit(0)

    file_path_str = sys.argv[1]
    
    try:
        parser = StepParser(Path(file_path_str))
        oriented = "--obb" in sys.argv
        
        print(f"Processing STEP file: {parser.step_path} (Oriented BBox: {oriented})")
        data = parser.extract_all_data(oriented_bbox=oriented)
        
        out_path = parser.step_path.with_suffix(".json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✅ Saved → {out_path}")
        print(f"Summary: {len(data.get('surfaces',[]))} surfaces, {len(data.get('edges',[]))} edges, {len(data.get('holes',[]))} holes processed.")

    except FileNotFoundError as e_fnf:
        print(f"Error: {e_fnf}", file=sys.stderr)
        sys.exit(1)
    except RuntimeError as e_rt:
        print(f"Runtime Error: {e_rt}", file=sys.stderr)
        sys.exit(1)
    except Exception as e_exc:
        print(f"An unexpected error occurred: {e_exc}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main_cli()