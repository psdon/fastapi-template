from fastapi import Depends, Security
from fastapi_auth0 import Auth0
from sqlmodel import Session
from {{cookiecutter.project_slug}}.config.env import settings
from {{cookiecutter.project_slug}}.repository.postgres.client import get_session
from {{cookiecutter.project_slug}}.repository.postgres.model import User
from {{cookiecutter.project_slug}}.repository.postgres.service.user import (
    get_or_create,
)

from ..schema.auth0_user import CurrentUser

auth = Auth0(domain=settings.AUTH0_DOMAIN, api_audience=settings.AUTH0_AUDIENCE, auth0user_model=CurrentUser)


def _current_user(session: Session = Depends(get_session), current_user: CurrentUser = Security(auth.get_user)) -> User:
    return get_or_create(session, current_user)


get_current_user = _current_user if settings.ENV not in ["unittest"] else lambda: None
