import sqlite3
import libsql_experimental as libsql

from tucon_backend.config import get_config


def get_db_connection() -> sqlite3.Connection:
    config = get_config()

    if config.ENV == "dev":
        return libsql.connect(config.TURSO_DB_PATH)

    url = config.TURSO_DATABASE_URL
    auth_token = config.TURSO_AUTH_TOKEN
    conn = libsql.connect(url, auth_token=auth_token)
    return conn
