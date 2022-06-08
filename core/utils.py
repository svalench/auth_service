import secrets
from datetime import datetime

import bcrypt
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette import status

from core.settings import settings


def decode_token(token):
    """Декодируем токен пользователя"""
    return jwt.decode(token, settings.secret_key, algorithms=settings.algorithm)


def get_password_hash(password):
    """Для хеширования пароля"""
    bytePwd = password.encode('utf-8')
    mySalt = bcrypt.gensalt()
    hash_pass = bcrypt.hashpw(bytePwd, mySalt)
    return hash_pass


def create_access_token(data, expires_delta):
    """Функция создает токен"""
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    access_token = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return access_token


def get_current_username(credentials: HTTPBasicCredentials = Depends(HTTPBasic())):
    """Защита документации"""
    correct_username = secrets.compare_digest(credentials.username, settings.docs_username)
    correct_password = secrets.compare_digest(credentials.password, settings.docs_password)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
