import os
from dataclasses import dataclass


def get_config():
    @dataclass
    class Config:
        ENV: str = os.getenv("ENV", "dev")
        TURSO_DB_PATH = "tucon.db"
        TURSO_DATABASE_URL: str = os.getenv("TURSO_DATABASE_URL", "")
        TURSO_AUTH_TOKEN: str = os.getenv("TURSO_AUTH_TOKEN", "")

    return Config()
