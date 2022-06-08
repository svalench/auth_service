from datetime import datetime

import bcrypt
import jwt

from core.settings import settings


def decode_token(token):
    return jwt.decode(token, settings.secret_key, algorithms=settings.algorithm)

def get_password_hash(password):
    """для хэширования пароля"""
    bytePwd = password.encode('utf-8')
    mySalt = bcrypt.gensalt()
    hash_pass = bcrypt.hashpw(bytePwd, mySalt)
    return hash_pass

def create_access_token(data, expires_delta):
    """ф-ия создает токен"""
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    access_token = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return access_token
