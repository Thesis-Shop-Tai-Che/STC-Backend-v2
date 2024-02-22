from datetime import datetime, timedelta
import random
import string

from jose import jwt, ExpiredSignatureError
from mailjet_rest import Client
from passlib.context import CryptContext

from config import settings
import requests

api_key = settings.MJ_APIKEY_PUBLIC
api_secret = settings.MJ_APIKEY_PRIVATE
mailjet = Client(auth=(api_key, api_secret), version="v3.1")

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(
    username: str = None,
    user_id: int = None,
    expires_delta: timedelta = None,
) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode = {"exp": expires_delta, "sub": str(username), "user_id": user_id}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)
    return encoded_jwt

def create_refresh_token(
    username: str = None,
    user_id: int = None,
    expires_delta: timedelta = None,
) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=REFRESH_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expires_delta, "sub": str(username), "user_id": user_id}
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_REFRESH_SECRET_KEY, settings.JWT_ALGORITHM
    )
    return encoded_jwt

def decode_and_verify_access_token(token):
    try:
        decoded_token = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return decoded_token
    except ExpiredSignatureError:
        return None
    except jwt.JWTError:
        return None
    
def decode_and_verify_refresh_token(token):
    try:
        decoded_token = jwt.decode(
            token,
            settings.JWT_REFRESH_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return decoded_token
    except ExpiredSignatureError:
        return None
    except jwt.JWTError:
        return None

def get_hashed_password(password: str):
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str):
    return password_context.verify(password, hashed_pass)

def generate_password(length):
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for _ in range(length))
    return password
