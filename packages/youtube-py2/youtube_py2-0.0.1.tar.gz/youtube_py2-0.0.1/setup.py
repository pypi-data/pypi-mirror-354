from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize
import sys
import os

# Cython拡張のビルド設定
ext_modules = cythonize([
    Extension(
        "youtube_py2",
        ["youtube_py2/__init__.py"],  # ←ここを修正
        extra_compile_args=["/O2"] if sys.platform == "win32" else ["-O2"],
    )
], compiler_directives={"language_level": "3"})

setup(
    name="youtube_py2",
    version="1.0.0",
    description="YouTube Data API v3 Python Wrapper Library (py2)",
    author="Himarry",
    author_email="",
    url="https://github.com/Himarry/youtube.py2",
    packages=find_packages(),
    install_requires=[],
    python_requires=">=3.8",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    ext_modules=ext_modules,
    zip_safe=False,
)
