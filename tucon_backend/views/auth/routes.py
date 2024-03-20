from flask import session
from werkzeug.exceptions import Conflict, Unauthorized
from tucon_backend import app
from tucon_backend.db import get_db_connection
from pydantic import BaseModel, EmailStr, Field, SecretStr
from flask_pydantic import validate
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from tucon_backend.middlewares.auth import login_required


class RegisterBody(BaseModel):
    name: str = Field(max_length=128)
    email: EmailStr = Field(max_length=128)
    password: SecretStr = Field(max_length=128)


def create_user(user: RegisterBody):
    conn = get_db_connection()

    user_with_email = conn.execute(
        "SELECT 1 FROM users WHERE email = ?", (user.email,)
    ).fetchone()

    if user_with_email:
        raise Conflict("User with this email already exists")

    ph = PasswordHasher()
    hashed_password = ph.hash(user.password.get_secret_value())

    row = conn.execute(
        "INSERT INTO users (name, email, password) VALUES (?, ?, ?) RETURNING id",
        (user.name, user.email, hashed_password),
    ).fetchone()
    conn.commit()

    user_id = row[0]

    return user_id


class LoginBody(BaseModel):
    email: EmailStr = Field(max_length=128)
    password: SecretStr = Field(max_length=128)


def login_user(user: LoginBody):
    conn = get_db_connection()
    user_with_email = conn.execute(
        "SELECT id, password FROM users WHERE email = ?", (user.email,)
    ).fetchone()
    user_id = user_with_email[0]
    user_password = user_with_email[1]

    if not user_with_email:
        raise Unauthorized("Email or password is invalid.")

    ph = PasswordHasher()
    try:
        ph.verify(user_password, user.password.get_secret_value())
    except VerifyMismatchError:
        raise Unauthorized("Email or password is invalid.")

    return user_id


@app.route("/register", methods=["POST"])
@validate()
def register(body: RegisterBody):
    user_id = create_user(body)
    session["user_id"] = user_id
    return {"user_id": user_id}, 201


@app.route("/login", methods=["POST"])
@validate()
def login(body: LoginBody):
    user_id = login_user(body)
    session["user_id"] = user_id
    return {"message": "ok"}, 200


@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user_id", default=None)
    return {"message": "ok"}, 200


@app.route("/me", methods=["GET"])
@login_required
def me(user_id: int):
    return {"user_id": user_id}, 200
