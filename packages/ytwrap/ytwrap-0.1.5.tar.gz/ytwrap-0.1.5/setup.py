from setuptools import setup, find_packages

setup(
    name="ytwrap",
    version="0.1.5",
    description="YouTube Data API v3 ラッパーライブラリ",
    author="Himarry",
    url="https://github.com/Himarry/ytwrap",
    project_urls={
        "Source": "https://github.com/Himarry/ytwrap",
        "Tracker": "https://github.com/Himarry/ytwrap/issues",
    },
    packages=find_packages(),
    install_requires=[
        "google-api-python-client"
    ],
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
