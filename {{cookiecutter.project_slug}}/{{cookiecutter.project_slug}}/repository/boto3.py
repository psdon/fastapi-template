import boto3
from {{cookiecutter.project_slug}}.config.env import settings

boto3_session = boto3.Session(aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
s3_client = boto3_session.client("s3")
s3_resource = boto3_session.resource("s3")
cognito_client = boto3_session.client("cognito-idp", region_name=settings.AWS_COGNITO_REGION)
