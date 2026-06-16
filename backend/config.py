import os
from dotenv import load_dotenv

# Load .env file if it exists (local development)
load_dotenv()

class Config:
    # Database - MUST be set in environment / .env file
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise RuntimeError(
            "DATABASE_URL environment variable is not set. "
            "Copy .env.example to .env and fill in your values."
        )

    # API key - MUST be set in environment / .env file
    API_KEY = os.getenv("API_KEY")
    if not API_KEY:
        raise RuntimeError(
            "API_KEY environment variable is not set. "
            "Copy .env.example to .env and fill in your values."
        )

    # Server (safe defaults - not secrets)
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))

config = Config()
