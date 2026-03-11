import time
import jwt
from os import getenv


def gerar_token():
    payload = {
        "iat": int(time.time())
    }
    return jwt.encode(payload, getenv("SECRET_KEY"), algorithm="HS256")