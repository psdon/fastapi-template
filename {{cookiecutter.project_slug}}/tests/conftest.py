import os
import sys

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel

path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, path + "/../")

from {{cookiecutter.project_slug}}.repository.postgres.client import get_session, db_engine
from mixer.backend.sqlalchemy import Mixer
from {{cookiecutter.project_slug}}.api import app


@pytest.fixture(scope="module")
def vcr_config():
    return {
        "filter_headers": [
            "Authorization",
            "X-Amz-Content-SHA256",
            "X-Amz-Date",
            "User-Agent",
            "amz-sdk-invocation-id",
            "amz-sdk-request",
        ]
    }


@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(db_engine)
    with Session(db_engine) as session:
        yield session

    session.close()
    SQLModel.metadata.drop_all(db_engine)


@pytest.fixture
def client(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def mixer(session: Session):
    return Mixer(session)
