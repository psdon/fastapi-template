import sys

from fastapi import FastAPI
from {{cookiecutter.project_slug}}.api import router
from {{cookiecutter.project_slug}}.api.app.cache import init_cache
from {{cookiecutter.project_slug}}.api.app.sentry import init_sentry
from {{cookiecutter.project_slug}}.config.env import Settings, settings
from loguru import logger
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from starlette.middleware.cors import CORSMiddleware
from toolz import pipe

from .cache import CacheControlMiddleware
from .root import router as root_router


def register_middlewares(app: FastAPI) -> FastAPI:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(SentryAsgiMiddleware)
    app.add_middleware(CacheControlMiddleware)
    return app


def create_instance(settings: Settings) -> FastAPI:
    return FastAPI(
        title=settings.APP_NAME,
        description=settings.DESCRIPTION,
        version=settings.VERSION,
        docs_url=None,  # Disable docs on main app
        redoc_url=None,
        openapi_url=None,
    )


def init_app(settings: Settings) -> FastAPI:
    if settings.ENV in ["testing", "staging", "production"]:
        init_sentry(settings)

    app: FastAPI = pipe(
        settings,
        create_instance,
        register_middlewares,
        router.register,
    )
    return app


logger.add(sys.stderr, backtrace=True, diagnose=True, level=settings.LOGGING_LEVEL)
app = init_app(settings)
app.include_router(root_router)


@app.on_event("startup")
async def startup_event():
    init_cache(settings)
