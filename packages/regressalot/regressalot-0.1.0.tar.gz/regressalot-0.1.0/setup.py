from setuptools import setup, find_packages

setup(
    name="regressalot",
    version="0.1.0",
    author="Ivan Levchenko",
    description="Simple AutoML tool for running and comparing ML models.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/o01qw/regressalot",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "scikit-learn",
        "matplotlib",
        "xgboost"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
