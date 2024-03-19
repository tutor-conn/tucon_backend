from tucon_backend import app
from tucon_backend.config import get_config

@app.route('/', methods=['GET'])
def index():
    config = get_config()
    return f'Welcome to Tucon backend! env={config.ENV}'
