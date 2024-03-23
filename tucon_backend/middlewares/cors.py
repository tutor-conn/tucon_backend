from tucon_backend import app
from tucon_backend.config import get_config
from flask_cors import CORS

config = get_config()

CORS(app, origins=config.CORS_ORIGIN)
