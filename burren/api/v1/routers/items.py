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


@router.get('/', response_model=List[schemas.ObjectData])
async def list_items(skip: int = 0, limit: int = 100,
                     db: Session = Depends(database.get_db)):
    items = crud.list_objectdata(db, skip=skip, limit=limit)
    return items


@router.post('/', response_model=schemas.ObjectData)
async def create_item(item: schemas.ObjectDataCreate,
                      db: Session = Depends(database.get_db)):
    owner = crud.get_user(db, user_id=item.owner_id)
    if owner is None:
        raise HTTPException(status_code=404, detail="Owner not found")

    db_item = crud.create_objectdata(db, item)
    return db_item


@router.get('/{item_id}', response_model=schemas.ObjectData)
async def get_item(item_id: str,
                   db: Session = Depends(database.get_db)):
    db_item = crud.get_objectdata(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item
