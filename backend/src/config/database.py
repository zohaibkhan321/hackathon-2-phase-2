# src/config/database.py
from sqlmodel import create_engine, Session
from typing import Generator
import os

# Use DATABASE_URL from env (set in your shell or .env)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://neondb_owner:npg_MWgTXphxZ6u5@ep-frosty-bar-adwmsz2y-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
)

# Create SQLModel engine with connection pooling for Neon
# echo=True for SQL logging during development; set False in production
engine = create_engine(
    DATABASE_URL, 
    echo=True,
    pool_pre_ping=True,  # Check connection before using
    pool_recycle=300,    # Recycle connections every 5 minutes
    connect_args={
        "sslmode": "require",
        "sslcert": None,
        "sslkey": None,
        "sslrootcert": None,
    }
)

def get_session() -> Generator[Session, None, None]:
    """
    Session generator for dependency injection.
    Usage: `db: Session = Depends(get_session)`
    """
    with Session(engine) as session:
        yield session
