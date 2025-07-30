from setuptools import setup, find_packages

setup(
    name="alumath-matmult",  # Package name on PyPI
    version="0.1.0",         # Initial version
    packages=find_packages(),  # Automatically find packages in the folder
    description="A simple Python package for matrix operations",
    long_description=open("README.md").read(),  # Use README as long description
    long_description_content_type="text/markdown",  # Markdown format for README
    author="Group 16",
    author_email="j.nformi1@alustudent.com",
    url="https://github.com/LaurelleJinelle/alumath_matmult.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
