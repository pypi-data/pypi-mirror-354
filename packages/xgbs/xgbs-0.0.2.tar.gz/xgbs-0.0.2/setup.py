from setuptools import setup, find_packages

setup(
    name="xgbs",
    version="0.0.2",
    author="Chuanyu Cui",
    description="XGBS: Classification Task-Driven Hyperspectral Band Selection via Interpretability from XGBoost",
    long_description="XGBS: Classification Task-Driven Hyperspectral Band Selection via Interpretability from XGBoost",
    url="https://https://github.com/FunctionMayBeStatic/XGBS",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[
        "scikit-learn==1.6.1",
        "xgboost==2.1.1",
    ]
)
