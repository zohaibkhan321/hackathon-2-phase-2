# src/config/logging.py
import logging

def setup_logging():
    """
    Simple logging setup. Expand as needed (handlers/formatters).
    Called during startup in lifespan.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )
    # Optional: control SQLAlchemy logging
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
