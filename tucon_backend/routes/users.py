from werkzeug.exceptions import Conflict, Unauthorized
from tucon_backend import app
from tucon_backend.db import get_db_connection
from pydantic import BaseModel, EmailStr, Field, SecretStr
from flask_pydantic import validate
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


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

    return row[0]


@app.route("/register", methods=["POST"])
@validate()
def register(body: RegisterBody):
    user_id = create_user(body)
    return {"user_id": user_id}, 201


class LoginBody(BaseModel):
    email: EmailStr = Field(max_length=128)
    password: SecretStr = Field(max_length=128)


def login_user(user: LoginBody):
    conn = get_db_connection()
    user_with_email = conn.execute(
        "SELECT id, password FROM users WHERE email = ?", (user.email,)
    ).fetchone()

    if not user_with_email:
        raise Unauthorized("Email or password is invalid.")

    ph = PasswordHasher()
    try:
        ph.verify(user.password.get_secret_value(), user_with_email["password"])
    except VerifyMismatchError:
        raise Unauthorized("Email or password is invalid.")

    return user_with_email["id"]


@app.route("/login", methods=["POST"])
@validate()
def login(body: LoginBody):
    login_user(body)
    return {"message": "ok"}, 200


@app.route("/users", methods=["GET"])
def get_users():
    conn = get_db_connection()
    users = conn.execute("SELECT email FROM users").fetchall()
    return users
