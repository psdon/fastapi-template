from redis import asyncio as aioredis
from {{cookiecutter.project_slug}}.config.env import settings

redis_client = aioredis.from_url(settings.REDIS_URL, encoding="utf8", decode_responses=True)
