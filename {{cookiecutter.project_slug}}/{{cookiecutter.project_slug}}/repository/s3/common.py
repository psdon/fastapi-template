import pandas as pd
from {{cookiecutter.project_slug}}.repository.boto3 import s3_client
from {{cookiecutter.project_slug}}.config.env import settings
from loguru import logger


def read_csv_to_dataframe(key) -> pd.DataFrame:
    try:
        result = s3_client.get_object(Bucket=settings.S3_BUCKET, Key=key)
        result = pd.read_csv(result.get("Body"), header=0)
        return result
    except s3_client.exceptions.NoSuchKey:
        logger.debug("S3 object not found")
        return pd.DataFrame()
