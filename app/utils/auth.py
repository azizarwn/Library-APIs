from datetime import datetime, timedelta

import bcrypt
from fastapi import HTTPException
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWSSignatureError

from app.core.settings import settings


def hash_password(plain_password: str) -> str:
    # Hash the password using bcrypt
    # plain_password is str, need to encode it to bytes.
    # encode defaults using UTF-8, which is standard for text data.
    # result of hashpw is bytes, decode it back to str for storage in the database.
    return bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt()).decode()


def is_password_valid(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


def generate_token(data: dict):
    copied_data = data.copy()
    copied_data["exp"] = datetime.utcnow() + timedelta(minutes=settings.JWT_EXP_MINUTES)
    return jwt.encode(copied_data, settings.SECRET_KEY, algorithm="HS256")


def validate_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload.get("id", None)
    except JWSSignatureError as e:
        print(f"Token validation error: {e}")
        return None
    except ExpiredSignatureError as e:
        print(f"Token expired: {e}")
        raise HTTPException(status_code=401, detail="Token has expired")
    except Exception as e:
        print(f"Unexpected error during token validation: {e}")
        return None
