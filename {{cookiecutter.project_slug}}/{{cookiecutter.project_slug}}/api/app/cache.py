import hashlib
from hashlib import md5
from typing import Optional

from fastapi import Request, Response
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware
from {{cookiecutter.project_slug}}.config.constants import NON_CACHE_KEYS
from {{cookiecutter.project_slug}}.config.env import Settings
from {{cookiecutter.project_slug}}.repository.redis.client import redis_client


class PatchFastAPICache(FastAPICache):

    # Patched for clearing cache on all namespaces
    # https://github.com/long2ice/fastapi-cache/issues/17#issuecomment-1038599763
    @classmethod
    async def clear(cls, namespace: str = "", key: str = ""):
        namespace = cls._prefix + ":" + (namespace or "") if not key else ""
        return await cls._backend.clear(namespace, key)


def key_builder(
    func,
    namespace: Optional[str] = "",
    request: Optional[Request] = None,
    response: Optional[Response] = None,
    args: Optional[tuple] = None,
    kwargs: Optional[dict] = None,
):
    kwargs = {key: kwargs[key] for key in kwargs if key not in NON_CACHE_KEYS}  # remove non-cache keys
    prefix = f"{FastAPICache.get_prefix()}:{namespace}:"
    cache_key = prefix + hashlib.md5(f"{func.__module__}:{func.__name__}:{args}:{kwargs}".encode()).hexdigest()
    return cache_key


@cache()
async def get_etag(response_body):
    value = md5(response_body.encode("utf-8")).hexdigest()
    return f'W\\"{value}"'


class CacheControlMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)
        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk
        response_body = response_body.decode()

        request_etag = request.headers.get("if-none-match")
        current_etag = await get_etag(response_body)
        if request_etag == current_etag:
            return Response(status_code=304, headers={"etag": current_etag, "cache-control": "public, max-age: 15780000"})

        if "etag" not in response.headers:
            response.headers["etag"] = current_etag
            response.headers["cache-control"] = "public, max-age: 15780000"

        return Response(
            content=response_body,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type,
        )


def init_cache(settings: Settings):
    if settings.CACHED_ENABLE is False:
        logger.debug("Caching is disabled")

    FastAPICache.init(
        RedisBackend(redis_client),
        prefix="{{cookiecutter.project_slug}}-cache",
        expire=86400,
        enable=settings.CACHED_ENABLE,
        key_builder=key_builder,
    )
