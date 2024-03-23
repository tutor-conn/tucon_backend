from tucon_backend import app
from flask_cors import CORS

CORS(app, supports_credentials=True)
