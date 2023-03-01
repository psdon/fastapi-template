from pydantic import BaseSettings, Field
from typing import Optional
import toml
from loguru import logger
import pathlib


class Settings(BaseSettings):
    API_PREFIX = "{{cookiecutter.api_prefix}}"

    ENV: str = Field("development")
    DEBUG: bool = Field(False)

    AWS_REGION: Optional[str]
    AWS_ACCESS_KEY_ID: Optional[str]
    AWS_SECRET_ACCESS_KEY: Optional[str]

    POSTGRES_URL: str = Field("postgresql://root:changeme@localhost:5432/{{cookiecutter.project_slug}}")
    REDIS_URL: str = Field("redis://localhost")

    # Load app name, version, commit variables from config file, for Sentry and health
    project = toml.load("./pyproject.toml")["tool"]["poetry"]
    APP_NAME = project["name"]
    VERSION = project["version"]
    DESCRIPTION = project["description"]

    try:
        commit_file = toml.load("./commit.toml")
    except FileNotFoundError:
        logger.warning("Couldn't load commit.toml")
        commit_file = {}

    COMMIT_ID: Optional[str] = commit_file.get("commit_id")
    BRANCH_NAME: Optional[str] = commit_file.get("branch_name")

    SENTRY_DSN = ""
    LOGGING_LEVEL: str = Field("INFO")
    LIMIT_PER_PAGE = 10000
    CACHED_ENABLE = Field(True)

    AUTH0_DOMAIN: str
    AUTH0_AUDIENCE: str = Field("http://localhost:8000")
    AUTH0_CLIENT_ID: str
    AUTH0_RULE_NAMESPACE: str = Field("https://example.com")

    class Config:
        env_file = f"{pathlib.Path(__file__).resolve().parent.parent.parent}/.env"


settings = Settings()