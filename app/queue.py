import redis.asyncio as redis
import json
from app.config import settings
from app.models import QueueItem


class RedisQueue:
    def __init__(self):
        self.redis_url = settings.redis_url
        self.queue_key = "instagram_queue"
        self.redis = None

    async def get_redis(self):
        if self.redis is None:
            self.redis = redis.from_url(self.redis_url)
        return self.redis

    async def enqueue(self, item: QueueItem):
        """Add item to queue"""
        redis_conn = await self.get_redis()
        data = item.dict()
        await redis_conn.rpush(self.queue_key, json.dumps(data))

    async def dequeue(self) -> QueueItem:
        """Remove and return item from queue"""
        redis_conn = await self.get_redis()
        data = await redis_conn.blpop(self.queue_key, timeout=1)
        if data:
            return QueueItem(**json.loads(data[1].decode('utf-8')))
        return None

    async def get_queue_length(self) -> int:
        """Get current queue length"""
        redis_conn = await self.get_redis()
        return await redis_conn.llen(self.queue_key)


queue = RedisQueue()
