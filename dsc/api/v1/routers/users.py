from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from dsc.db import crud
from dsc.db import database
from dsc.db import schemas

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
