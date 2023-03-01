"""Special routes that is available globally"""

import humps
from fastapi import APIRouter
from {{cookiecutter.project_slug}}.config.env import settings

from .cache import PatchFastAPICache
from .health import ping_postgres, ping_redis

router = APIRouter(prefix=settings.API_PREFIX)


@router.get("/health-check")
async def health_check_endpoint():
    """
    Display basic health check
    """
    postgres_status = await ping_postgres()
    redis_status = await ping_redis()

    return humps.camelize(
        {
            "app_name": settings.APP_NAME,
            "environment": settings.ENV,
            "version": settings.VERSION,
            "branch": settings.BRANCH_NAME,
            "commit_id": settings.COMMIT_ID,
            "aws_region": settings.AWS_REGION,
            "postgres": postgres_status,
            "redis": redis_status,
        }
    )


@router.get("/clear-cached")
async def clear_cached():
    """Clear cached across namespaces"""
    return await PatchFastAPICache.clear()
