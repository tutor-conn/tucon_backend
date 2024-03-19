from tucon_backend import app
from pydantic import BaseModel
from flask_pydantic import validate

class UserCreateBody(BaseModel):
    email: str
    password: str

@app.route('/users', methods=['POST'])
@validate()
def post_users(body: UserCreateBody):
    return { "message": "post_users", "body": body.model_dump() }

@app.route('/users', methods=['GET'])
def get_users():
    return 'get_users'
