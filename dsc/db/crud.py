from datetime import datetime
from datetime import timedelta
import uuid

from sqlalchemy.orm import Session

from dsc.db import models
from dsc.db import schemas
from dsc.utils import pwdtools


def get_user_by_id(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_name(db: Session, name: str):
    return db.query(models.User).filter(models.User.name == name).first()


def get_user(db: Session, hint: str):
    for f in [get_user_by_id, get_user_by_email, get_user_by_name]:
        db_user = f(db, hint)
        if db_user:
            return db_user
    return None


def list_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwdtools.salted_hash(user.password)
    db_user = models.User(id=str(uuid.uuid4()),
                          name=user.name,
                          fullname=user.fullname,
                          email=user.email,
                          hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_from_token(db: Session, token: str):
    db_token = db.query(models.Token).filter(models.Token.id == token).first()
    if not db_token:
        return None
    if db_token.expires_at > datetime.now():
        return False
    return get_user_by_id(db, token.user_id)


def create_token(db: Session, user_id: str):
    token_id = str(uuid.uuid4())
    created_at = datetime.now()
    expires_at = created_at + timedelta(minutes=30)
    db_token = models.Token(id=token_id,
                            created_at=created_at,
                            expires_at=expires_at,
                            user_id=user_id)
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token


def get_session(db: Session, session_id: str):
    return db.query(models.Session).filter(
            models.Session.id == session_id).first()


def list_sessions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Session).offset(skip).limit(limit).all()


def create_session(db: Session, session: schemas.SessionCreate):
    session_id = str(uuid.uuid4())
    new_session = session.dict()
    members = [new_session.owner]
    tags = []
    if getattr(new_session, 'members', None):
        members += new_session.pop("members")
    if getattr(new_session, 'tags', None):
        tags = new_session.pop("tags")
    db_session = models.Session(id=session_id,
                                **new_session)
    for member in members:
        db_member = get_user(db, member)
        if db_member:
            db_session.members.append(db_member)
    for tag in tags:
        db_tag = get_tag(db, tag)
        if db_tag:
            db_session.tags.append(db_tag)
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session


def get_image(db: Session, image_id: str):
    return db.query(models.Image).filter(models.Image.id == image_id).first()


def list_images(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Image).offset(skip).limit(limit).all()


def create_image(db: Session, image: schemas.ImageCreate):
    image_id = str(uuid.uuid4())
    new_image = image.dict()
    tags = []
    image_models = []
    if getattr(new_image, 'tags', None):
        tags = new_image.pop("tags")
    if getattr(new_image, 'model_ids', None):
        models = new_image.pop("model_ids")
    db_image = models.Image(id=image_id,
                            **new_image)
    for tag in tags:
        db_tag = get_tag(db, tag)
        if db_tag:
            db_image.tags.append(db_tag)
    for model in image_models:
        db_model = get_user(db, model)
        if db_model:
            db_image.models.append(db_model)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image


def get_tag(db: Session, tag_name: str):
    return db.query(models.Tag).filter(models.Tag.name == tag_name).first()


def list_tags(db: Session, skip: int = 0, limit: int = 0):
    return db.query(models.Tag).offset(skip).limit(limit).all()


def create_tag(db: Session, tag: schemas.TagCreate):
    db_tag = models.Tag(**tag.dict())
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


def get_objectdata(db: Session, object_id: str):
    return db.query(models.ObjectData).filter(
            models.ObjectData.id == object_id).first()


def list_objectdata(db: Session, skip: int = 0, limit: int = 0):
    db.query(models.ObjectData).offset(skip).limit(limit).all()


def create_objectdata(db: Session,
                      objectdata: schemas.ObjectData):
    object_id = str(uuid.uuid4())
    db_object = models.Session(id=object_id,
                               **objectdata.dict())
    db.add(db_object)
    db.commit()
    db.refresh(db_object)
    return db_object
