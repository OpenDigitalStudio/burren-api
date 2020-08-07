from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm

from dsc.db import crud
from dsc.db import database
from dsc.db import models
from dsc.utils import pwdtools

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="userauth/token")


async def get_current_user(db: Session = Depends(database.get_db),
                           token: str = Depends(oauth2_scheme)):
    user = crud.get_user_from_token(db, token)
    return user


@router.get('/me')
async def get_me(current_user: models.User = Depends(get_current_user)):
    return current_user


@router.get('/test')
async def test_endpoint(token: str = Depends(oauth2_scheme)):
    return {'token': token}


@router.post('/token')
async def login(db: Session = Depends(database.get_db),
                form_data: OAuth2PasswordRequestForm = Depends()):
    db_user = crud.get_user_by_name(form_data.username)
    if pwdtools.check_password(form_data.password,
                               getattr(db_user, "hashed_password", "")):
        return {'access_token': crud.create_token(db, db_user.id),
                'token_type': 'bearer'}
    else:
        return HTTPException(status_code=400,
                             detail="Username or password is invalid")
