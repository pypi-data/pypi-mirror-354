from pydantic import BaseSettings

class S3Settings(BaseSettings):
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_region: str = "us-east-1"
    bucket_name: str
    allowed_extensions: list[str] = ["jpg", "png", "pdf", "docx"]
    max_file_size_mb: int = 10

    class Config:
        env_file = ".env"

s3_settings = S3Settings()
