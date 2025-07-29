from setuptools import setup, find_packages

setup(
    name="osunbit", 
    version="0.0.1",
    packages=find_packages(),
    author="Your Name",
    description="Basic Osunbit SDK for Python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=["Programming Language :: Python :: 3"],
    python_requires=">=3.6",
)
