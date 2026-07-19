from pathlib import Path
from setuptools import setup, find_packages

README = Path("README.md").read_text(encoding="utf-8")

setup(
    name="eggcrypt",
    version="3.2.0",
    packages=find_packages(),
    description="A pretty secure (yet inefficient) encryption program.",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Egglord",
    license="MIT", 
    license_files=("LICENSE",),
    python_requires=">=3.7",
)
