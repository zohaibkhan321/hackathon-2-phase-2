# src/api/dependencies.py
from typing import Generator
from sqlmodel import Session
from ..config.database import get_session

def get_db() -> Generator[Session, None, None]:
    """
    Adapter dependency that yields DB session.
    Keeps the API surface simple and stable.
    """
    yield from get_session()
