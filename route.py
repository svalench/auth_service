from datetime import timedelta

import bcrypt
import jwt
from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi_viewsets import BaseViewset, create_element
from fastapi_viewsets.db_conf import Base, engine, get_session
from starlette import status

from model import User
from schema import UserSchema
from utils import get_password_hash, create_access_token, decode_token

router = APIRouter()

Base.metadata.create_all(engine)  # created table in db (by default this is sqlite3 base.db)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

protected_user_model = BaseViewset(endpoint='/user',
                                   model=User,
                                   response_model=UserSchema,
                                   db_session=get_session,
                                   tags=['users']
                                   )

protected_user_model.register(methods=['LIST', 'GET', 'PATCH'],
                              protected_methods=['LIST', 'GET', 'PATCH'],
                              oauth_protect=oauth2_scheme)


@router.post('/user', tags=['users'])
def add_user(user: UserSchema, token: str = Depends(oauth2_scheme)):
    """точка добавления пользователя"""
    data = user.dict()
    if not data.get('password'):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='not correct password')
    data['password'] = get_password_hash(data['password'])
    removed = data.clear()
    return create_element(data=data, model=User, db_session=get_session)

@router.get('/getme', tags=['users'])
def getme(token: str = Depends(oauth2_scheme)):
    """Получить информацию об авторизованном пользователе"""
    try:
        data = decode_token(token)
        return get_session().query(User).filter(User.id == data.get('id')).first()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post('/token', tags=['auth'])
def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """генерит токен для пользователя"""
    user_form = UserSchema(username=form_data.username, password=form_data.password)
    user = get_session().query(User).filter(User.username == user_form.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='username is incorrect'
        )
    if bcrypt.checkpw(user_form.password.encode('utf8'), user.password.encode('utf8')):
        access_token_expires = timedelta(minutes=60 * 5)
        access_token = create_access_token(data={"user": user.username, "id": user.id},
                                           expires_delta=access_token_expires)
        return {'access_token': access_token, 'token_type': 'bearer'}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='password is incorrect'
        )
