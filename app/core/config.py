import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


class Settings:
    api_key = os.getenv("DEEPSEEK_API_KEY")
    base_url = os.getenv("AI_BASE_URL", "https://api.deepseek.com")
    model = os.getenv("AI_MODEL", "deepseek-flash")
    database_name = str(PROJECT_ROOT / "chat.db")


settings = Settings()
