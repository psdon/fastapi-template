from datetime import datetime

from {{cookiecutter.project_slug}}.config.utils import datetime_utc
from sqlmodel import Field

from .base import BaseModel


class User(BaseModel, table=True):
    auth0_id: str = Field(index=True, unique=True)
    email: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime_utc)
    updated_at: datetime = Field(default_factory=datetime_utc)
