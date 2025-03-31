import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).resolve().parent.parent

ENV_PATH = BASE_DIR / ".env"

load_dotenv(ENV_PATH)


class GigaChatSettings(BaseSettings):
    api_key: str = os.getenv("GIGACHAT_API_KEY")
    scope: str = os.getenv("GIGACHAT_SCOPE")


class Settings(BaseSettings):
    giga_chat: GigaChatSettings = GigaChatSettings()


settings = Settings()
