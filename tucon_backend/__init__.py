from flask import Flask, json
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

# ======== Middlewares ========
import tucon_backend.middlewares.cors
import tucon_backend.middlewares.flask_session

# ======== Routes      ========
import tucon_backend.views.index

import tucon_backend.views.profiles
import tucon_backend.views.auth


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps(
        {
            "code": e.code,
            "name": e.name,
            "description": e.description,
        }
    )
    response.content_type = "application/json"
    return response
