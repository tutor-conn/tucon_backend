from functools import wraps

from flask import session
from werkzeug.exceptions import Unauthorized


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        session_user_id = session.get("user_id")
        if session_user_id is None:
            raise Unauthorized("Must be logged in to access this resource.")
        return f(*args, user_id=session_user_id, **kwargs)

    return decorated
