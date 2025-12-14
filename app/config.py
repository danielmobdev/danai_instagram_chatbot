from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Instagram API
    instagram_access_token: str = ""
    instagram_business_id: str = ""
    instagram_app_id: str = ""
    instagram_verify_token: str = "your_verify_token"
    instagram_app_secret: str = ""

    # Redis
    redis_url: str = "redis://localhost:6379"

    # AI
    gemini_api_key: str = ""

    # Rate limiting
    rate_limit_per_user: int = 10  # messages per hour
    rate_limit_window: int = 3600  # seconds

    # Anti-spam
    spam_threshold: int = 3  # repeated messages

    class Config:
        env_file = ".env"


settings = Settings()
