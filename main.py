import uuid
from datetime import timedelta, datetime
from typing import Optional
import bcrypt as bcrypt
import jwt as jwt
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi_viewsets import BaseViewset, create_element
from fastapi_viewsets.db_conf import Base, get_session, engine
from pydantic import BaseModel
from sqlalchemy import Column, String, Boolean
from starlette import status

from settings import Settings

settings = Settings(_env_file='.env', _env_file_encoding='utf-8')
app = FastAPI()


class UserSchema(BaseModel):
    """Pydantic Schema"""
    id: Optional[str]
    username: str
    password: str
    is_admin: Optional[bool]

    class Config:
        orm_mode = True


class User(Base):
    """SQLAlchemy model"""

    __tablename__ = "user"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True)
    password = Column(String(255))
    is_admin = Column(Boolean, default=False)


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


app.include_router(protected_user_model)

# other endpoints

secret_key = 'SECRET_KEY'

algorithm = "HS256"


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
    access_token = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return access_token


@app.post('/user', tags=['users'])
def add_user(user: UserSchema, token: str = Depends(oauth2_scheme)):
    """точка добавления пользователя"""
    data = user.dict()
    if not data.get('password'):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='not correct password')
    data['password'] = get_password_hash(data['password'])
    create_element(**data)

@app.get('/getme', tags=['users'])
def getme(token: str = Depends(oauth2_scheme)):
    """Получить информацию об авторизованном пользователе"""
    try:
        data = jwt.decode(token, secret_key, algorithms=algorithm)
        return get_session().query(User).filter(User.id == data.get('id')).first()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.post('/token', tags=['auth'])
def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """генерит ьтокен для пользователя"""
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

