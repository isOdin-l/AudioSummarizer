from pydantic import BaseModel
import os

class Settings(BaseModel):
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    API_BASE_URL: str = os.getenv("API_BASE_URL", "http://localhost:8000")
    SOURCE_TYPE: str = "telegram"

settings = Settings()
