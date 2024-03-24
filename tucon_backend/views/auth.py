from flask import session
from sqlalchemy import insert, select
from werkzeug.exceptions import Conflict, NotFound, Unauthorized
from tucon_backend import app
from tucon_backend.constants import UserHome
from tucon_backend.db import create_db_session
from pydantic import BaseModel, EmailStr, Field, SecretStr
from flask_pydantic import validate
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from tucon_backend.models import User


class RegisterBody(BaseModel):
    firstName: str = Field(max_length=64)
    lastName: str = Field(max_length=64)
    email: EmailStr = Field(max_length=128)
    password: SecretStr = Field(max_length=128)


def create_user(user: RegisterBody):
    conn = create_db_session()

    user_with_email = conn.execute(select(1).where(User.email == user.email)).fetchone()

    if user_with_email:
        raise Conflict("User with this email already exists")

    ph = PasswordHasher()
    hashed_password = ph.hash(user.password.get_secret_value())

    row = conn.execute(
        insert(User)
        .values(
            first_name=user.firstName,
            last_name=user.lastName,
            email=user.email,
            password=hashed_password,
            home=UserHome.Onboarding,
        )
        .returning(User.id)
    ).fetchone()
    conn.commit()

    if not row:
        raise Exception("Expected user id to be returned after insert.")

    user_id = row.tuple()[0]

    return user_id


class LoginBody(BaseModel):
    email: EmailStr = Field(max_length=128)
    password: SecretStr = Field(max_length=128)


def login_user(user: LoginBody):
    conn = create_db_session()

    user_with_email = conn.execute(
        select(User.id, User.password).where(User.email == user.email)
    ).fetchone()

    if not user_with_email:
        # Note: Return the same error message for both email and password to avoid leaking
        #       that this email exists in the system.
        raise Unauthorized("Incorrect email or password.")

    user_id, user_password = user_with_email.tuple()

    ph = PasswordHasher()
    try:
        ph.verify(user_password, user.password.get_secret_value())
    except VerifyMismatchError:
        raise Unauthorized("Incorrect email or password.")

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
    return {"message": "Logged in successfully"}


@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user_id", default=None)
    return {"message": "Logged out successfully"}


@app.route("/me", methods=["GET"])
def me():
    user_id = session.get("user_id")

    if user_id is None:
        return {"userId": None}

    conn = create_db_session()
    user = conn.execute(
        select(User.first_name, User.last_name, User.home).where(User.id == user_id)
    ).fetchone()

    if not user:
        raise NotFound("User from session not found")

    first_name, last_name, home = user.tuple()

    return {
        "userId": user_id,
        "firstName": first_name,
        "lastName": last_name,
        "home": home,
    }
