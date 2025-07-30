import aioboto3
from .config import s3_settings

def get_s3_client():
    return aioboto3.client(
        "s3",
        aws_access_key_id=s3_settings.aws_access_key_id,
        aws_secret_access_key=s3_settings.aws_secret_access_key,
        region_name=s3_settings.aws_region,
    )
