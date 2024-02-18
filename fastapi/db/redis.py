from redis.asyncio import Redis

from core.config import settings
from .storage_interface import StorageInterface


class AsyncRedisStorageEngine(StorageInterface):
    connection: Redis

    def __init__(self):
        self.connection = Redis(host=settings.redis_host, port=settings.redis_port)

    async def close(self) -> None:
        await self.connection.close()

    async def get_entry(self, key: str) -> str | None:
        return await self.connection.get(name=key)

    async def set_entry(self, key: str, value: str) -> None:
        await self.connection.set(name=key, value=value)
