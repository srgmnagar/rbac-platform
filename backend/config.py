import os

# This gives you the absolute path to the backend/ folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Config:
    # Database — always creates rbac.db inside backend/
    DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'rbac.db')}")
    
    # API
    API_KEY = os.getenv("API_KEY", "dev-key-12345")
    
    # Server
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))

config = Config()