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

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from burren.db import crud
from burren.db import database
from burren.db import schemas

router = APIRouter()


@router.get('/', response_model=List[schemas.User])
async def list_users(skip: int = 0, limit: int = 100,
                     db: Session = Depends(database.get_db)):
    users = crud.list_users(db, skip=skip, limit=limit)
    return users


@router.post('/', response_model=schemas.User)
async def create_user(user: schemas.UserCreate,
                      db: Session = Depends(database.get_db)):
    return crud.create_user(db, user)


@router.get('/{user}', response_model=schemas.User)
async def get_user(user: str,
                   db: Session = Depends(database.get_db)):
    if '@' in user:
        db_user = crud.get_user_by_email(db, email=user)
        if db_user is not None:
            return db_user
    if len(user) == 36:
        db_user = crud.get_user_by_id(db, user_id=user)
        if db_user is not None:
            return db_user
    db_user = crud.get_user_by_name(db, name=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
