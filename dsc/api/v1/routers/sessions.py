from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from dsc.db import crud
from dsc.db import database
from dsc.db import schemas

router = APIRouter()


@router.get('/', response_model=List[schemas.Session])
async def list_sessions(skip: int = 0, limit: int = 100,
                        db: Session = Depends(database.get_db)):
    sessions = crud.list_sessions(db, skip=skip, limit=limit)
    return sessions


@router.post('/', response_model=schemas.Session)
async def create_session(new_session: schemas.SessionCreate,
                         db: Session = Depends(database.get_db)):
    owner = crud.get_user(db, user_id=new_session.owner_id)
    if owner is None:
        raise HTTPException(status_code=404, detail="Owner not found")

    db_session = crud.create_session(db, new_session)
    return db_session


@router.get('/{session_id}', response_model=schemas.Session)
async def get_session(session_id: str,
                      db: Session = Depends(database.get_db)):
    db_session = crud.get_session(db, session_id=session_id)
    if db_session is None:
        raise HTTPException(status_code=404, detail="Sesssion not found")
    return db_session
