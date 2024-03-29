from typing import Union
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from fastapi import HTTPException, Depends, status

from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

# secret key obtained with $ openssl rand -hex 32
SECRET_KEY = "ca2b7f3a3fcc06efa59c8ee321b775e3b6b100cd11b20a8eb14d54e565ab494a"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# proof of concept users database
users_db = {
    "admin": {
        "username": "admin",
        "hashed_password": "$2b$12$76.bmmKZ.5l/Vv4bDTqOF.JKsELsFtuSMfWElAVO9VxnQNwN39Jl2",
    }
}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Pydantic models for the authentication
class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None

class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    """ Get a user from the database """
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """ Get logged in user from token"""
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


def verify_password(plain_password, hashed_password):
    """ Verify if password matches the stored hashed """
    return pwd_context.verify(plain_password, hashed_password)


def token_login(form_data: OAuth2PasswordRequestForm):
    """ Get a token with a username and password"""

    user = authenticate_user(users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


def authenticate_user(db, username: str, password: str):
    """ Authenticate a user with a username and password"""
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    """ Transform a dictionary into a JWT token """

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt