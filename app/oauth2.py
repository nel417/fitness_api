from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MIN = 5


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MIN)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exeception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exeception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exeception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exeption = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail=f"could not validate user",
                                         headers={"WWW-Authenticate": "Bearer"})
    return verify_access_token(token, credentials_exeption)
