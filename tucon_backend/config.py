import os
from dataclasses import dataclass
from typing import Literal, Optional


@dataclass
class Config:
    ENV: Literal["dev", "prod"]
    UPSTASH_REDIS_PORT: int
    UPSTASH_REDIS_HOST: str
    UPSTASH_REDIS_PASSWORD: str
    FLASK_SECRET_KEY: Optional[str]

    TURSO_DB_PATH = "tucon.db"
    CORS_ORIGIN: str = os.getenv("CORS_ORIGIN", "*")
    TURSO_AUTH_TOKEN: str = os.getenv("TURSO_AUTH_TOKEN", "")
    TURSO_DATABASE_URL: str = os.getenv("TURSO_DATABASE_URL", "")
    TURSO_AUTH_TOKEN: str = os.getenv("TURSO_AUTH_TOKEN", "")

    def __init__(self):
        env = os.getenv("ENV", "dev")
        assert env in ["dev", "prod"], "ENV must be 'dev' or 'prod'"
        self.ENV = env  # type: ignore

        redis_host = os.getenv("UPSTASH_REDIS_HOST")
        assert redis_host, "UPSTASH_REDIS_HOST must be set"
        self.UPSTASH_REDIS_HOST = redis_host

        redis_port = os.getenv("UPSTASH_REDIS_PORT")
        assert redis_port, "UPSTASH_REDIS_PORT must be set"
        assert redis_port.isdigit(), "UPSTASH_REDIS_PORT must be an integer"
        self.UPSTASH_REDIS_PORT = int(redis_port)

        redis_password = os.getenv("UPSTASH_REDIS_PASSWORD")
        assert redis_password, "UPSTASH_REDIS_PASSWORD must be set"
        self.UPSTASH_REDIS_PASSWORD = redis_password

        secret_key = os.getenv("FLASK_SECRET_KEY")
        if not secret_key and env == "prod":
            raise ValueError("FLASK_SECRET_KEY must be set in production")
        self.FLASK_SECRET_KEY = secret_key


_config: Optional[Config] = None


def get_config():
    global _config
    _config = _config or Config()
    return _config
