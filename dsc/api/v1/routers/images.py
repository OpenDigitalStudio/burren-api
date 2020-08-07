from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from dsc.db import crud
from dsc.db import database
from dsc.db import models
from dsc.db import schemas
from dsc.userauth import oauth2

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
