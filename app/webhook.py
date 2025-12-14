import hmac
import hashlib
from fastapi import HTTPException, Request
from app.config import settings
from app.queue import queue
from app.models import QueueItem
from app.rate_limit import rate_limiter


async def verify_webhook(request: Request, body: bytes) -> bool:
    """Verify webhook signature"""
    signature = request.headers.get('X-Hub-Signature-256')
    if not signature:
        return False

    expected_signature = hmac.new(
        settings.instagram_app_secret.encode(),
        body,
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(f"sha256={expected_signature}", signature)


async def handle_webhook(data: dict):
    """Process incoming webhook data"""
    if 'entry' not in data:
        return

    for entry in data['entry']:
        if 'messaging' in entry:
            for messaging_event in entry['messaging']:
                if 'message' in messaging_event and 'text' in messaging_event['message']:
                    sender_id = messaging_event['sender']['id']
                    message_text = messaging_event['message']['text']
                    timestamp = messaging_event['timestamp']
                    message_id = messaging_event['message']['mid']

                    # Temporarily disable rate limiting and spam checks for testing
                    # TODO: Fix Redis connection issues
                    # if await rate_limiter.is_rate_limited(sender_id):
                    #     print(f"Rate limited: {sender_id}")
                    #     continue
                    # if await rate_limiter.is_spam(sender_id, message_text):
                    #     print(f"Spam detected: {sender_id}")
                    #     continue

                    # Queue the message for processing
                    item = QueueItem(
                        user_id=sender_id,
                        message_text=message_text,
                        timestamp=timestamp,
                        message_id=message_id
                    )
                    await queue.enqueue(item)
