from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
# Read the README file for the long description
long_description = (here / "README.md").read_text(encoding="utf-8")
setup(
    name="fastapi-async-s3uploader",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "aioboto3>=10.4.0",
        "fastapi>=0.95",
        "pydantic>=1.10",
    ],
    author="Md Anisur Rahman",
    description="A reusable file uploader package for FastAPI and AWS S3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
)
