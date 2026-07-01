import os
from dotenv import load_dotenv

# Load .env file if it exists (local development).
# Copy .env.example to .env and fill in your values — never commit .env.
load_dotenv()


class Config:
    # Database — MUST be provided via environment variable or .env file.
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    if not DATABASE_URL:
        raise RuntimeError(
            "DATABASE_URL is not set.\n"
            "Copy .env.example to .env and fill in your values:\n"
            "  cp .env.example .env"
        )

    # API key — MUST be provided via environment variable or .env file.
    API_KEY: str = os.getenv("API_KEY", "")
    if not API_KEY:
        raise RuntimeError(
            "API_KEY is not set.\n"
            "Copy .env.example to .env and fill in your values:\n"
            "  cp .env.example .env"
        )

    # Server (safe non-secret defaults)
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))


config = Config()
