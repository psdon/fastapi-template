from {{cookiecutter.project_slug}}.repository.redis.client import redis_client
from {{cookiecutter.project_slug}}.repository.postgres.client import db_engine


async def ping_postgres():
    try:
        conn = db_engine.connect()
        conn.close()
        return "Online"
    except Exception:
        return "Offline"


async def ping_redis():
    try:
        await redis_client.ping()
        return "Online"
    except Exception:
        return "Offline"
