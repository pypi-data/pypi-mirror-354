from setuptools import setup, find_packages

long_description = (
    "ytwrap is a general-purpose Python wrapper library for the YouTube Data API v3. "
    "It allows you to easily retrieve and analyze YouTube video and comment data, "
    "and access various YouTube Data API v3 features from Python."
)

setup(
    name="ytwrap",
    version="0.1.6",
    description="A general-purpose Python wrapper library for the YouTube Data API v3. Easily retrieve and analyze YouTube video and comment data, and access various YouTube Data API v3 features from Python.",
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
    long_description=long_description,
    long_description_content_type="text/markdown",
)
