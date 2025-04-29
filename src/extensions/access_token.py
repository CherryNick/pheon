from datetime import datetime

import jwt
from pydantic import BaseModel


class AccessToken(BaseModel):
    sub: str
    exp: datetime
    iat: datetime


def decode_access_token(secret_key: str, token: str) -> AccessToken:
    payload = jwt.decode(token, secret_key, algorithms=["HS256"])
    return AccessToken(**payload)
