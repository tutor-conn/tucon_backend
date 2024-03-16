from tucon_backend.db import get_connection
from dotenv import load_dotenv
import sys

load_dotenv()


def run_sqlscript(filename: str):
    conn = get_connection()

    with open(filename, "r") as f:
        contents = f.read()
    conn.executescript(contents)

    print("Script ran successfully")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python exec_sql.py <filename.sql>")
        sys.exit(1)

    filename = sys.argv[1]

    run_sqlscript(filename)
