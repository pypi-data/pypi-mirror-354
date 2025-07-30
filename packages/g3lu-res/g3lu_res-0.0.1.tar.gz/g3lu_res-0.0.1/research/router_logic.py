import json
import numpy as np
import torch
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForCausalLM
import os
from typing import Tuple # 반환 타입 명시를 위해 추가

EMBEDDING_MODEL_NAME = 'BM-K/KoSimCSE-roberta-multitask'
LLM_MODEL_NAME = 'davidkim205/komt-llama2-7b-v1'
FALLBACK_LOWER_BOUND = 0.40
FALLBACK_UPPER_BOUND = 0.55

class QueryRouter:
    """
    오픈소스 모델을 사용한 Query Router 클래스.
    이 클래스의 인스턴스는 한 번 생성되어 재사용됩니다.
    """
    def __init__(self, data_path: str):
        print("--- Query Router 초기화 시작 (from router_logic.py) ---") # 어느 파일에서 로드되는지 확인용
        data_dir = os.path.dirname(data_path)
        if data_dir and not os.path.exists(data_dir):
            print(f"경고: 데이터 디렉토리 '{data_dir}'를 찾을 수 없어 생성합니다.")
            os.makedirs(data_dir, exist_ok=True)

        if not os.path.exists(data_path):
            print(f"경고: '{data_path}'를 찾을 수 없습니다. 테스트용 임시 파일을 생성합니다.")
            dummy_data = {
                "inspection_samples": [
                    {"text": "표면이 긁혔어", "label": "surface"},
                    {"text": "모서리가 깨졌어", "label": "edge"},
                    {"text": "구멍 직경이 이상해", "label": "hole"},
                    # ... (기존 dummy_data 내용)
                ]
            }
            with open(data_path, 'w', encoding='utf-8') as f:
                json.dump(dummy_data, f, ensure_ascii=False, indent=4)
            print(f"임시 데이터 파일 생성 완료: {data_path}")

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"사용 장치: {self.device}")

        self._load_data(data_path)
        self._init_embedding_model()
        self._init_classifier()
        self._init_fallback_llm()
        print("--- Query Router 초기화 완료 (from router_logic.py) ---")

    def _load_data(self, data_path: str):
        print(f"1. 데이터 로드 중... ({data_path})")
        with open(data_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)['inspection_samples']
        self.texts = [item['text'] for item in self.data]
        self.labels = [item['label'] for item in self.data]
        if not self.texts or not self.labels:
            raise ValueError("데이터 파일에서 텍스트 또는 레이블을 로드하지 못했습니다. 파일 내용을 확인하세요.")
        print(f"데이터 로드 완료. 총 {len(self.texts)}개 샘플.")

    def _init_embedding_model(self):
        print(f"2. 임베딩 모델 로드 중... ({EMBEDDING_MODEL_NAME})")
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME, device=self.device)

    def _init_classifier(self):
        print("3. k-NN 분류기 준비 중...")
        self.label_encoder = LabelEncoder()
        if not self.labels:
            raise ValueError("k-NN 분류기 학습을 위한 레이블 데이터가 없습니다.")
        y_train = self.label_encoder.fit_transform(self.labels)
        
        print("   - 예문 데이터 임베딩 중...")
        if not self.texts:
            raise ValueError("k-NN 분류기 학습을 위한 텍스트 데이터가 없습니다.")
        X_train = self.embedding_model.encode(self.texts, show_progress_bar=True, batch_size=128)
        
        num_samples = len(X_train)
        if num_samples == 0:
            raise ValueError("임베딩된 학습 데이터가 없어 k-NN 분류기를 초기화할 수 없습니다.")
        
        k_value = min(3, num_samples) 
        if k_value == 0 : k_value = 1

        self.knn_classifier = KNeighborsClassifier(n_neighbors=k_value, metric='cosine') 
        self.knn_classifier.fit(X_train, y_train)
        print(f"k-NN 분류기 준비 완료. k={k_value}, 학습된 레이블: {self.label_encoder.classes_}")

    def _init_fallback_llm(self):
        print(f"4. Fallback LLM 로드 중... ({LLM_MODEL_NAME})")
        try:
            print("   - ⚠️  이 과정은 몇 분 정도 소요될 수 있으며, 많은 메모리가 필요합니다.")
            self.llm_tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL_NAME)
            self.llm_model = AutoModelForCausalLM.from_pretrained(
                LLM_MODEL_NAME,
                torch_dtype=torch.bfloat16 if self.device == "cuda" and torch.cuda.is_bf16_supported() else torch.float32,
                device_map="auto"
            )
            print("   - Fallback LLM 로드 성공.")
        except ImportError:
            print(f"   - Fallback LLM ({LLM_MODEL_NAME}) 로딩에 필요한 라이브러리가 없습니다. (transformers 등)")
            print("   - Fallback 기능 없이 라우터를 계속 진행합니다.")
            self.llm_model = None
            self.llm_tokenizer = None
        except Exception as e:
            print(f"   - Fallback LLM 로드 중 예기치 않은 오류 발생: {e}")
            print("   - Fallback 기능 없이 라우터를 계속 진행합니다.")
            self.llm_model = None
            self.llm_tokenizer = None

    def _ask_llm(self, query: str) -> str:
        if not self.llm_model or not self.llm_tokenizer:
            return "unknown"

        prompt = f"""다음 사용자 문의를 'surface', 'edge', 'hole' 중 하나의 카테고리로 분류해주세요.
사용자 문의: "{query}"
카테고리:"""

        inputs = self.llm_tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512).to(self.device)
        
        try:
            output_ids = self.llm_model.generate(
                **inputs,
                max_new_tokens=10, 
                pad_token_id=self.llm_tokenizer.eos_token_id,
                num_beams=3, 
                early_stopping=True
            )
            response_ids = output_ids[0][inputs.input_ids.shape[-1]:]
            response = self.llm_tokenizer.decode(response_ids, skip_special_tokens=True).strip()
        except Exception as e:
            print(f"LLM 생성 중 오류: {e}")
            return "unknown"

        cleaned_response = response.lower()
        for label in self.label_encoder.classes_:
            if label.lower() in cleaned_response:
                return label 
        return "unknown"

    def route(self, query: str) -> Tuple[str, str]:
        print(f"\n- 라우팅할 쿼리: '{query}'")
        
        query_vector = self.embedding_model.encode([query], show_progress_bar=False)
        
        probabilities = self.knn_classifier.predict_proba(query_vector)
        top_proba = np.max(probabilities)
        
        predicted_class_index = self.knn_classifier.predict(query_vector)[0]
        predicted_label_by_knn = self.label_encoder.inverse_transform([predicted_class_index])[0]
        
        print(f"   - 1차 분류(k-NN): '{predicted_label_by_knn}' (신뢰도: {top_proba:.2f})")
        
        final_decision = predicted_label_by_knn
        reason = "k-NN Classifier"

        if self.llm_model and self.llm_tokenizer and FALLBACK_LOWER_BOUND < top_proba < FALLBACK_UPPER_BOUND:
            print(f"   - 신뢰도({top_proba:.2f})가 애매한 구간({FALLBACK_LOWER_BOUND}~{FALLBACK_UPPER_BOUND})입니다. LLM에 재질문합니다.")
            llm_decision = self._ask_llm(query)
            print(f"   - LLM 분류 결과: '{llm_decision}'")
            if llm_decision != "unknown" and llm_decision in self.label_encoder.classes_:
                final_decision = llm_decision
                reason = "LLM Fallback"
            else:
                reason = "k-NN (LLM Fallback 실패 또는 유효하지 않은 답변)"
        elif FALLBACK_LOWER_BOUND < top_proba < FALLBACK_UPPER_BOUND:
                 print(f"   - 신뢰도({top_proba:.2f})가 애매한 구간이지만, LLM이 없어 k-NN 결과를 사용합니다.")
        
        print(f" 최종 결정: {final_decision} (근거: {reason})")
        return final_decision, reason