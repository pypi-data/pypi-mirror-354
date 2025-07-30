import os
import uuid
from fastapi import UploadFile, HTTPException
from .config import s3_settings

def validate_file(file: UploadFile):
    ext = file.filename.split(".")[-1].lower()
    if ext not in s3_settings.allowed_extensions:
        raise HTTPException(status_code=400, detail="Unsupported file extension")

def generate_unique_filename(original: str) -> str:
    ext = original.split(".")[-1]
    return f"{uuid.uuid4().hex}.{ext}"

async def validate_file_size(file: UploadFile):
    contents = await file.read()
    max_size = s3_settings.max_file_size_mb * 1024 * 1024
    if len(contents) > max_size:
        raise HTTPException(status_code=413, detail="File too large")
    await file.seek(0)
