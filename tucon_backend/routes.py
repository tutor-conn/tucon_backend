import os
from tucon_backend import app
from tucon_backend.db import get_connection


@app.route("/")
def index():
    return {"message": "Tucon API", "env": os.getenv("ENV")}


@app.route("/users")
def users():
    conn = get_connection()
    users = conn.execute("select * from users").fetchall()
    return {"message": users}
