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


@router.get('/', response_model=List[schemas.Tag])
async def list_tags(skip: int = 0, limit: int = 100,
                    db: Session = Depends(database.get_db)):
    tags = crud.list_tags(db, skip=skip, limit=limit)
    return tags


@router.post('/', response_model=schemas.Tag)
async def create_tag(tag: schemas.TagCreate,
                     db: Session = Depends(database.get_db)):

    db_tag = crud.create_tag(db, tag)
    return db_tag


@router.get('/{image_id}', response_model=schemas.Tag)
async def get_tag(tag_name: str,
                  db: Session = Depends(database.get_db)):
    db_tag = crud.get_tag(db, tag_name=tag_name)
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return db_tag
