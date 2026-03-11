import jwt
from flask import current_app

def create_jwt(user_id, role):
    payload = {"user_id": user_id, "role": role}
    token = jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")
    return token

def decode_jwt(token):
    return jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
