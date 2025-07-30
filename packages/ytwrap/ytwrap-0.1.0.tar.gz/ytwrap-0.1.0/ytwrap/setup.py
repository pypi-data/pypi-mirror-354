from setuptools import setup, find_packages

setup(
    name="ytwrap",
    version="0.1.0",
    description="YouTube Data API v3 ラッパーライブラリ",
    author="Himarry",
    packages=find_packages(),
    install_requires=[
        "google-api-python-client"
    ],
    python_requires=">=3.7",
)
