from setuptools import setup, find_packages

setup(
    name="fastapi-async-s3uploader",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "aioboto3>=10.4.0",
        "fastapi>=0.95",
        "pydantic>=1.10",
    ],
    author="Md Anisur Rahman",
    description="A reusable file uploader package for FastAPI and AWS S3",
    include_package_data=True,
)
