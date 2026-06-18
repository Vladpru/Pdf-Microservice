import os
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    pdf_service_secret: str
    pdf_internal_secret: str
    token_ttl_seconds: int = 3600
    pdf_service_base_url: str = Field(
        default_factory=lambda: os.getenv("RENDER_EXTERNAL_URL", "http://localhost:8000")
    )

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
