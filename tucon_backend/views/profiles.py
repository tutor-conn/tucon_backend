from typing import Optional

from sqlalchemy import insert, update
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import Conflict
from tucon_backend import app
from tucon_backend.constants import ProfileType, LastView
from tucon_backend.db import create_db_session
from pydantic import BaseModel, Field
from flask_pydantic import validate
from tucon_backend.models import Profile, User

from tucon_backend.middlewares.auth import login_required


class CreateStudentProfileBody(BaseModel):
    bio: Optional[str] = Field(max_length=1024, default=None)
    payRate1: Optional[float] = Field(ge=0, default=None)
    payRate2: Optional[float] = Field(ge=0, default=None)
    city: Optional[str] = Field(max_length=128, default=None)


class CreateTutorProfileBody(BaseModel):
    bio: Optional[str] = Field(max_length=1024, default=None)
    payRate: float = Field(ge=0)
    city: Optional[str] = Field(max_length=128, default=None)


def create_student_profile(user_id: int, profile: CreateStudentProfileBody):
    session = create_db_session()

    try:
        session.execute(
            insert(Profile).values(
                user_id=user_id,
                profile_type=ProfileType.Student,
                bio=profile.bio,
                pay_rate1=profile.payRate1,
                pay_rate2=profile.payRate2,
                city=profile.city,
            )
        )
    except IntegrityError:
        raise Conflict("Student profile already exists")
    session.execute(
        update(User).where(User.id == user_id).values(last_view=LastView.StudentHome)
    )
    session.commit()


def create_tutor_profile(user_id: int, profile: CreateTutorProfileBody):
    session = create_db_session()

    try:
        session.execute(
            insert(Profile).values(
                user_id=user_id,
                profile_type=ProfileType.Tutor,
                bio=profile.bio,
                pay_rate1=profile.payRate,
                pay_rate2=None,
                city=profile.city,
            )
        )
    except IntegrityError:
        raise Conflict("Tutor profile already exists")
    session.execute(
        update(User).where(User.id == user_id).values(last_view=LastView.TutorHome)
    )
    session.commit()


@app.route("/profiles/student", methods=["POST"])
@login_required
@validate()
def post_profiles_student(user_id: int, body: CreateStudentProfileBody):
    create_student_profile(user_id, body)
    return {"message": "Student profile created successfully"}, 201


@app.route("/profiles/tutor", methods=["POST"])
@login_required
@validate()
def post_profiles_tutor(user_id: int, body: CreateTutorProfileBody):
    create_tutor_profile(user_id, body)
    return {"message": "Tutor profile created successfully"}, 201
