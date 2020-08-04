from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from dsc.db import crud
from dsc.db import database
from dsc.db import schemas

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
