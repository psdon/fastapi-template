FROM python:3.11.1-slim
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"
ENV ENV=production

RUN apt update \
    && apt install --no-install-recommends -y \
        curl \
        build-essential \
        libyaml-dev \
        default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry - respects $POETRY_VERSION & $POETRY_HOME
ENV POETRY_VERSION=1.1.13
RUN curl -sSL https://install.python-poetry.org | python3 -

# We copy our Python requirements here to cache them
# and install only runtime deps using poetry
WORKDIR $PYSETUP_PATH
COPY ./pyproject.toml ./
COPY ./poetry.lock ./

RUN poetry install --no-dev --no-root  # respects

WORKDIR /app
COPY . .

CMD ["uvicorn", "scripts.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
