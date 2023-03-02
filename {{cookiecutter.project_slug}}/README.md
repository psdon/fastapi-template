# {{ cookiecutter.project_slug }}
## Installation
Install `poetry` and dev dependencies
```shell
poetry install
```

Initialize pre-commit hooks
```shell
pre-commit install
```

Start local services
```shell
docker-compose up -d
```

Configure environment variables
```shell
cp .env.sample .env
```

Start development server
```shell
poetry run server
```

Open Swagger Docs on the browser
```commandline
http://localhost:8000{{ cookiecutter.api_prefix }}/v1/internal/docs
```


## Testing
Run unit test
```
ENV=unittest pytest .
```
