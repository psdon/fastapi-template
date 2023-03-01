from typing import Optional

from fastapi_auth0 import Auth0User
from pydantic import Field
from {{cookiecutter.project_slug}}.config.env import settings


class CurrentUser(Auth0User):
    auth0_id: str = Field(..., alias="sub")
    email: Optional[str] = Field(None, alias=f"{settings.AUTH0_RULE_NAMESPACE}/email")
