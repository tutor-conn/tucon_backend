from typing import Optional
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session

from tucon_backend.config import get_config

_engine: Optional[Engine] = None


def get_engine():
    global _engine

    config = get_config()

    dbUrl = f"sqlite+{config.TURSO_DATABASE_URL}/?authToken={config.TURSO_AUTH_TOKEN}&secure=true"

    # use local sqlite db in dev
    if config.ENV == "dev":
        dbUrl = f"sqlite:///{config.TURSO_DB_PATH}"

    _engine = _engine or create_engine(
        dbUrl, connect_args={"check_same_thread": False}, echo=(config.ENV == "dev")
    )

    return _engine


def create_db_session():
    return Session(get_engine())
