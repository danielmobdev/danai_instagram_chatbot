import asyncio
import json
import redis.asyncio as redis
import time
from app.config import settings
from app.queue import queue
from app.ai import ai_responder
from app.instagram import instagram_client
from app.models import ConversationMessage


class ConversationStore:
    def __init__(self):
        self.redis_url = settings.redis_url
        self.redis = None

    async def get_redis(self):
        if self.redis is None:
            self.redis = redis.from_url(self.redis_url)
        return self.redis

    async def get_conversation(self, user_id: str) -> list[ConversationMessage]:
        """Get conversation history for user"""
        redis_conn = await self.get_redis()
        key = f"conversation:{user_id}"
        data = await redis_conn.lrange(key, 0, -1)
        return [ConversationMessage(**json.loads(msg.decode('utf-8'))) for msg in data]

    async def add_message(self, user_id: str, message: ConversationMessage):
        """Add message to conversation"""
        redis_conn = await self.get_redis()
        key = f"conversation:{user_id}"
        await redis_conn.rpush(key, json.dumps(message.dict()))
        # Keep only last 50 messages
        await redis_conn.ltrim(key, -50, -1)


conversation_store = ConversationStore()


async def process_queue():
    """Background worker to process queued messages"""
    while True:
        item = await queue.dequeue()
        if item:
            # Temporarily disable conversation retrieval for testing
            # TODO: Fix Redis connection issues
            conversation = []  # Empty conversation for testing

            # Temporarily disable conversation storage for testing
            # TODO: Fix Redis connection issues
            # user_msg = ConversationMessage(
            #     role="user",
            #     content=item.message_text,
            #     timestamp=item.timestamp
            # )
            # await conversation_store.add_message(item.user_id, user_msg)

            # Generate AI response
            ai_response = await ai_responder.generate_response(conversation, item.message_text)

            # Send response via Instagram
            success = await instagram_client.send_message(item.user_id, ai_response)

            if success:
                # Temporarily disable AI response storage for testing
                # TODO: Fix Redis connection issues
                # ai_msg = ConversationMessage(
                #     role="assistant",
                #     content=ai_response,
                #     timestamp=int(time.time() * 1000)  # current time in ms
                # )
                # await conversation_store.add_message(item.user_id, ai_msg)
                print(f"Responded to {item.user_id}: {ai_response}")
            else:
                print(f"Failed to send message to {item.user_id}")

        await asyncio.sleep(0.1)  # Small delay to prevent busy loop


async def start_worker():
    """Start the background worker"""
    asyncio.create_task(process_queue())
