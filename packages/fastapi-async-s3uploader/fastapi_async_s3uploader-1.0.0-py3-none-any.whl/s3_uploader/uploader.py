from typing import List, Optional
from fastapi import UploadFile
from .client import get_s3_client
from .utils import validate_file, validate_file_size, generate_unique_filename
from .config import s3_settings


async def upload_file_to_s3(file: UploadFile, folder: str = "uploads") -> str:
    validate_file(file)
    await validate_file_size(file)

    filename = generate_unique_filename(file.filename)
    key = f"{folder}/{filename}"

    async with get_s3_client() as s3:
        await s3.upload_fileobj(file.file, s3_settings.bucket_name, key)
        url = f"https://{s3_settings.bucket_name}.s3.{s3_settings.aws_region}.amazonaws.com/{key}"
        return url


async def upload_multiple_files_to_s3(
    files: List[UploadFile], folder: str = "uploads"
) -> List[str]:
    return [await upload_file_to_s3(file, folder) for file in files]


async def upload_dynamic(
    file: Optional[UploadFile] = None,
    files: Optional[List[UploadFile]] = None,
    folder: str = "uploads",
) -> List[str]:
    if file:
        return [await upload_file_to_s3(file, folder)]
    elif files:
        return await upload_multiple_files_to_s3(files, folder)
    else:
        raise ValueError("No file(s) provided")


# New function to delete file from S3 by its key
async def delete_file_from_s3(key: str):
    async with get_s3_client() as s3:
        await s3.delete_object(Bucket=s3_settings.bucket_name, Key=key)
