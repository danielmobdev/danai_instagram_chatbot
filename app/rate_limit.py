import redis.asyncio as redis
import time
import hashlib
from app.config import settings


class RateLimiter:
    def __init__(self):
        self.redis_url = settings.redis_url
        self.redis = None

    async def get_redis(self):
        if self.redis is None:
            self.redis = redis.from_url(self.redis_url)
        return self.redis

    async def is_rate_limited(self, user_id: str) -> bool:
        """Check if user is rate limited"""
        redis_conn = await self.get_redis()
        key = f"rate_limit:{user_id}"
        current_time = int(time.time())

        # Get current count and reset time
        data = await redis_conn.hgetall(key)
        if not data:
            # First request
            await redis_conn.hset(key, mapping={"count": 1, "reset_time": current_time + settings.rate_limit_window})
            return False

        count = int(data[b'count'].decode('utf-8'))
        reset_time = int(data[b'reset_time'].decode('utf-8'))

        if current_time > reset_time:
            # Reset window
            await redis_conn.hset(key, mapping={"count": 1, "reset_time": current_time + settings.rate_limit_window})
            return False

        if count >= settings.rate_limit_per_user:
            return True

        # Increment count
        await redis_conn.hincrby(key, "count", 1)
        return False

    async def is_spam(self, user_id: str, message_text: str) -> bool:
        """Check if message is spam (repeated)"""
        redis_conn = await self.get_redis()
        key = f"spam:{user_id}"
        message_hash = hashlib.md5(message_text.encode()).hexdigest()

        # Count occurrences of this message in last hour
        count = await redis_conn.zcount(key, "-inf", "+inf")
        if count >= settings.spam_threshold:
            return True

        # Add message with timestamp
        await redis_conn.zadd(key, {message_hash: int(time.time())})
        # Expire after 1 hour
        await redis_conn.expire(key, 3600)
        return False


rate_limiter = RateLimiter()
