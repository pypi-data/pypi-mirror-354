from setuptools import setup, find_packages

setup(
    name='g3lu_res',
    version='0.0.1',
    description='PYPI tutorial package creation written by G3LU',
    author='G3LU',
    author_email='leejyoung0325@gmail.com',
    url='https://github.com/G3LU/Research',
    install_requires=['tqdm','scikit-learn',],
    packages=find_packages(exclude=[]),
    keywords=['python'],
    python_requires='>=3.8',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
