import time
from typing import Dict

import jwt

from app.config import get_auth_data


def token_response(token: str):
    return {
        "access_token": token
    }

def signJWT(user_data: dict) -> Dict[str, str]:
    payload = {
        "user_id": user_data['user_id'],
        "username": user_data['username'],
        "expires": time.time() + 9000
    }
    auth_data = get_auth_data()
    token = jwt.encode(payload, auth_data['secret_key'], algorithm=auth_data['algorithm'])

    return token_response(token)

def decodeJWT(token: str) -> dict:
    auth_data = get_auth_data()
    try:
        decoded_token = jwt.decode(token, auth_data['secret_key'], algorithms=[auth_data['algorithm']])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}