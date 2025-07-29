from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="onnx-shape-fix",
    version="0.2.1",
    description="A tool to fix shape information in ONNX models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Hafiz",
    author_email="hafizabc77@gmail.com",
    url="https://github.com/hafizabc77/onnx-shape-fix",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "onnx-shape-fix=onnx_shape_fix.cli:main",
        ],
    },
)
