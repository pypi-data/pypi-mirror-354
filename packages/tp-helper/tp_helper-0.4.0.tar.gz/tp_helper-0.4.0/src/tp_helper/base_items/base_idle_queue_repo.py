from redis.asyncio import Redis
from tp_helper.base_items.base_queue_repo import BaseQueueRepo

class BaseIdleQueueRepo(BaseQueueRepo):
    def __init__(self, name: str, redis_client: Redis):
        super().__init__(f"{name}:idle", redis_client)

    async def signal(self):
        await self.redis_client.rpush(self.queue_name, "")

    async def wait(self, timeout: int = 0, clear: bool = True) -> str | None:
        result = await self.redis_client.blpop([self.queue_name], timeout=timeout)
        if result is None:
            return None
        _, data = result
        if clear:
            await self.redis_client.delete(self.queue_name)
        return str(data)
