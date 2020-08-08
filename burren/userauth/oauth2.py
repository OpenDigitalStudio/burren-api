# Copyright (c) 2020 Erno Kuvaja OpenDigitalStudio.net
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import List
from typing import Optional

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm

from burren.db import crud
from burren.db import database
from burren.db import schemas
from burren.utils import pwdtools

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="userauth/token")


async def get_current_user(db: Session = Depends(database.get_db),
                           token: str = Depends(oauth2_scheme)):
    user = crud.get_user_from_token(db, token)
    cred_exc = HTTPException(status_code=401,
                             detail="Token is invalid",
                             headers={"WWW-Authenticate": "Bearer"})
    if not user:
        raise cred_exc
    return user


async def validate_token(db: Session = Depends(database.get_db),
                         token: str = Depends(oauth2_scheme),
                         user: schemas.User = Depends(get_current_user)):
    return token


@router.get('/me', response_model=schemas.User)
async def get_me(current_user: schemas.User = Depends(get_current_user)):
    return current_user


@router.get('/test')
async def test_endpoint(token: str = Depends(validate_token)):
    return {'token': token}


@router.post('/token')
async def login(db: Session = Depends(database.get_db),
                form_data: OAuth2PasswordRequestForm = Depends()):
    db_user = crud.get_user_by_name(db=db, name=form_data.username)
    if pwdtools.check_passwd(form_data.password,
                             getattr(db_user, "hashed_password", "")):
        return {'access_token': crud.create_token(db, db_user.id).id,
                'token_type': 'bearer'}
    else:
        raise HTTPException(status_code=400,
                            detail="Username or password is invalid")


@router.get('/token', response_model=List[schemas.Token])
async def list_user_tokens(db: Session = Depends(database.get_db),
                           curr_user: schemas.User = Depends(get_current_user),
                           skip: Optional[int] = 0,
                           limit: Optional[int] = 100):
    return crud.list_user_tokens(db=db, user_id=curr_user.id, skip=skip,
                                 limit=limit)


@router.delete('/token/{token}', status_code=204)
async def delete_user_token(token: str, db: Session = Depends(database.get_db),
                            curr_usr: schemas.User = Depends(get_current_user)
                            ):
    result = crud.delete_user_token(db=db,
                                    token_id=token,
                                    user_id=curr_usr.id)
    if not result:
        return HTTPException(status_code=404, detail="Token not found.")
