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
from burren.db import models
from burren.db import schemas
from burren.userauth import oauth2

router = APIRouter()


@router.get('/', response_model=List[schemas.Image])
async def list_images(skip: int = 0, limit: int = 100,
                      db: Session = Depends(database.get_db),
                      user: models.User = Depends(oauth2.get_current_user)):
    images = crud.list_images(db, skip=skip, limit=limit, qfilter=user.id)
    return images


@router.post('/', response_model=schemas.Image)
async def create_image(image: schemas.ImageCreate,
                       db: Session = Depends(database.get_db),
                       user: models.User = Depends(oauth2.get_current_user)):

    db_image = crud.create_image(db=db, image=image, owner=user.id)
    return db_image


@router.get('/{image_id}', response_model=schemas.Image)
async def get_image(image_id: str,
                    db: Session = Depends(database.get_db)):
    db_image = crud.get_image(db, image_id=image_id)
    if db_image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return db_image
