from flask import Flask

app = Flask(__name__)

import tucon_backend.routes.index
import tucon_backend.routes.users
