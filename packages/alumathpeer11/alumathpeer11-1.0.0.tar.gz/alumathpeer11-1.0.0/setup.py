from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="alumathpeer11",
    version="1.0.0",
    author="alumathpeer11 Team",
    author_email="i.mugisha@alustudent.com",
    description="Pure Python matrix operations library without external dependencies",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Mugisha-isaac/ALU_Formatie_2",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        # "Topic :: Mathemtatics for machine learning",
    ],
    python_requires=">=3.7",
    install_requires=[],  # No external dependencies
    keywords="matrix, multiplication, linear algebra, mathematics",
)