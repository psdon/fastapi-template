from fastapi import FastAPI
from {{cookiecutter.project_slug}}.config.env import settings

from .sample import router as sample_router

if settings.ENV in ("development", "staging", "testing"):
    api_v1 = FastAPI(
        title=settings.APP_NAME,
        description=settings.DESCRIPTION,
        version=settings.VERSION,
        docs_url="/internal/docs",  # TODO: blocked in WAF
        redoc_url="/internal/redoc",
        openapi_url="/internal/openapi.json",
        debug=settings.DEBUG,
    )
else:
    api_v1 = FastAPI(
        title=settings.APP_NAME,
        description=settings.DESCRIPTION,
        version=settings.VERSION,
        docs_url=None,  # Disable docs on main app
        redoc_url=None,
        openapi_url=None,
    )
api_v1.include_router(sample_router, tags=["sample"])


def register(app: FastAPI) -> FastAPI:
    app.mount(f"{settings.API_PREFIX}/v1", api_v1)
    return app
