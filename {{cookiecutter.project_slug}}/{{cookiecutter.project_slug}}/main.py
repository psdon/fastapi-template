import subprocess

import uvicorn
from {{cookiecutter.project_slug}}.repository.postgres import client, model


def dev_server():
    uvicorn.run("{{cookiecutter.project_slug}}.api.app:app", host="0.0.0.0", port=8000, reload=True, log_level="debug")


def run_tests():
    """
    Run all unittests. Equivalent to:
    `ENV=unittest poetry run pytest .`
    """
    subprocess.run(["ENV=unittest", "python", "-u", "-m", "pytest", "."])


def init_db():
    model.BaseModel.metadata.create_all(client.db_engine)


if __name__ == "__main__":
    dev_server()
