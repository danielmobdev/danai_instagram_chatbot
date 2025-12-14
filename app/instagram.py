import httpx
from app.config import settings


class InstagramClient:
    def __init__(self):
        self.base_url = "https://graph.facebook.com/v18.0"
        self.access_token = settings.instagram_access_token
        self.business_id = settings.instagram_business_id

    async def send_message(self, recipient_id: str, message_text: str) -> bool:
        """Send message to Instagram user"""
        url = f"{self.base_url}/{self.business_id}/messages"
        params = {
            "access_token": self.access_token
        }
        data = {
            "recipient": {"id": recipient_id},
            "message": {"text": message_text}
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, params=params, json=data)
                response.raise_for_status()
                return True
            except httpx.HTTPStatusError as e:
                print(f"Error sending message: {e}")
                print(f"Response body: {response.text}")
                return False
            except Exception as e:
                print(f"Unexpected error: {e}")
                return False


instagram_client = InstagramClient()
