import os
from pathlib import Path
from dotenv import load_dotenv

from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).resolve().parent.parent.parent

ENV_PATH = BASE_DIR / ".env"

load_dotenv(ENV_PATH)


class GigaChatSettings(BaseSettings):
    API_KEY: str = os.getenv("GIGACHAT_API_KEY")
    SCOPE: str = os.getenv("GIGACHAT_SCOPE")
    CLIENT_ID: str = os.getenv("GIGACHAT_CLIENT_ID")
    CLIENT_SECRET: str = os.getenv("GIGACHAT_CLIENT_SECRET")
