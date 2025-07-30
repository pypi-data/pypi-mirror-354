# setup.py
from setuptools import setup, find_packages

setup(
    name="credit-risk-creditum",
    version="0.1.0",
    author="Omoshola Owolabi",
    author_email="owolabi.omoshola.simon@gmail.com",
    description="A comprehensive credit risk assessment framework",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/omoshola-o/credit-risk-creditum",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    install_requires=[
        "numpy>=1.19.0",
        "pandas>=1.2.0",
        "scikit-learn>=0.24.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "isort>=5.0",
        ],
    },
)