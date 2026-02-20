import redis.asyncio as redis
from app.core.config import settings

async def get_redis():
    client = redis.from_url(str(settings.REDIS_URL))
    try:
        yield client
    finally:
        await client.close()
