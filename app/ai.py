import google.generativeai as genai
from app.config import settings
from app.models import ConversationMessage
from typing import List


class AIResponder:
    def __init__(self):
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    async def generate_response(self, conversation: List[ConversationMessage], user_message: str) -> str:
        """Generate AI response based on conversation history"""
        # Build prompt with conversation context
        prompt = "You are a helpful Instagram chatbot. Respond naturally and engagingly.\n\n"
        prompt += "Conversation history:\n"
        for msg in conversation[-10:]:  # Last 10 messages for context
            role = "User" if msg.role == "user" else "Assistant"
            prompt += f"{role}: {msg.content}\n"
        prompt += f"User: {user_message}\nAssistant:"

        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            # Fallback response
            return "Sorry, I'm having trouble responding right now. Please try again later."


ai_responder = AIResponder()
