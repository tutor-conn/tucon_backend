from flask import Flask
import os

app = Flask(__name__)


@app.route("/")
def index():
    return "Welcome to Tucon! api.tucon.ca"


# This is used for local development and not used when deploying through Cloud Run
if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
