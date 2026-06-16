from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import QueuePool
from .config import config

# PostgreSQL with connection pooling (production-grade)
engine = create_engine(
    config.DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,              # Keep 10 connections ready
    max_overflow=20,           # Allow up to 20 more if needed
    pool_recycle=3600,         # Recycle connections every 1 hour
    echo=False                 # Set True for SQL debugging
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
