import os
from typing import List

from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME = "ScreenGuide AI Layer"
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    ALLOWED_ORIGINS = [
        origin.strip()
        for origin in os.getenv("ALLOWED_ORIGINS", "*").split(",")
        if origin.strip()
    ]


settings = Settings()
