from tucon_backend.db import get_connection
from dotenv import load_dotenv
import sys

load_dotenv()


def push_db():
    conn = get_connection()

    with open("tucon_backend/schema.sql", "r") as f:
        sql = f.read()

    conn.executescript(sql)

    print("Database pushed successfully")


def seed_db():
    conn = get_connection()

    with open("tucon_backend/seed.sql", "r") as f:
        sql = f.read()

    conn.executescript(sql)

    print("Database seeded successfully")


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ["push", "seed"]:
        print("Usage: python db_control.py [push|seed]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "push":
        push_db()

    if command == "seed":
        seed_db()
