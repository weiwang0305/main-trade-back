import os
from typing import ClassVar

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings"""

    # Schwab API settings
    SCHWAB_APP_KEY: str = os.getenv("SCHWAB_APP_KEY", "")
    SCHWAB_APP_SECRET: str = os.getenv("SCHWAB_APP_SECRET", "")
    SCHWAB_CALLBACK_URL: str = os.getenv("SCHWAB_CALLBACK_URL", "")
    ALPACA_API_KEY: str = os.getenv("ALPACA_API_KEY", "")
    ALPACA_SECRET_KEY: str = os.getenv("ALPACA_SECRET_KEY", "")
    POLYGON_API_KEY: str = os.getenv("POLYGON_API_KEY", "")
    TOKEN_PATH: str = "tmp/token.json"

    # API settings
    API_TITLE: str = "Schwab Trading API"
    API_DESCRIPTION: str = "A FastAPI application for Schwab trading operations"
    API_VERSION: str = "1.0.0"

    # CORS settings
    ALLOWED_ORIGINS: ClassVar[list] = ["*"]  # Configure properly for production


settings = Settings()
