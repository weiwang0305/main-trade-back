from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    """Application settings"""
    
    # Schwab API settings
    SCHWAB_APP_KEY: str = os.getenv('SCHWAB_APP_KEY', '')
    SCHWAB_APP_SECRET: str = os.getenv('SCHWAB_APP_SECRET', '')
    SCHWAB_CALLBACK_URL: str = os.getenv('SCHWAB_CALLBACK_URL', '')
    TOKEN_PATH: str = 'tmp/token.json'
    
    # API settings
    API_TITLE: str = "Schwab Trading API"
    API_DESCRIPTION: str = "A FastAPI application for Schwab trading operations"
    API_VERSION: str = "1.0.0"
    
    # CORS settings
    ALLOWED_ORIGINS: list = ["*"]  # Configure properly for production

settings = Settings()
