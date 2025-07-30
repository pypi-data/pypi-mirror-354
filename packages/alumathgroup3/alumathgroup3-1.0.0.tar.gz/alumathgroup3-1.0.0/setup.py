from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="alumathgroup3",
    version="1.0.0",
    author="Group 3",
    author_email="erneste.ntezirizaza@gmail.com",
    description="A simple Python library for matrix multiplication",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/InshutiSouvede/Formative-2-Peer-Group-3",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    python_requires=">=3.6",
    keywords="matrix multiplication linear algebra math",
    project_urls={
        "Bug Reports": "https://github.com/InshutiSouvede/Formative-2-Peer-Group-3/issues",
        "Source": "https://github.com/InshutiSouvede/Formative-2-Peer-Group-3",
    },
)
