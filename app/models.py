from pydantic import BaseModel
from typing import List, Optional


class WebhookEntry(BaseModel):
    id: str
    time: int
    messaging: List[dict]


class WebhookMessage(BaseModel):
    sender: dict
    recipient: dict
    timestamp: int
    message: dict


class ConversationMessage(BaseModel):
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: int


class QueueItem(BaseModel):
    user_id: str
    message_text: str
    timestamp: int
    message_id: str


class RateLimitData(BaseModel):
    count: int
    reset_time: int
