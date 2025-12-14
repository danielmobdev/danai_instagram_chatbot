import asyncio
from app.models import QueueItem


class InMemoryQueue:
    """Temporary in-memory queue for testing without Redis"""

    def __init__(self):
        self.queue = asyncio.Queue()

    async def enqueue(self, item: QueueItem):
        """Add item to queue"""
        await self.queue.put(item)

    async def dequeue(self) -> QueueItem:
        """Remove and return item from queue"""
        try:
            return self.queue.get_nowait()
        except asyncio.QueueEmpty:
            return None

    async def get_queue_length(self) -> int:
        """Get current queue length"""
        return self.queue.qsize()


# Temporarily use in-memory queue for testing
# TODO: Fix Redis connection issues
queue = InMemoryQueue()
