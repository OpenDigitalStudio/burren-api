from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import relationship

from dsc.db import database


image_tags = Table('image_tags', database.Base.metadata,
                   Column('image_id', String(36), ForeignKey('images.id')),
                   Column('tag_id', String(20), ForeignKey('tags.name')))

image_models = Table('image_models', database.Base.metadata,
                     Column('image_id', String(36), ForeignKey('images.id')),
                     Column('user_id', String(36), ForeignKey('users.id')))

session_members = Table('session_members', database.Base.metadata,
                        Column('session_id', String(36),
                               ForeignKey('sessions.id')),
                        Column('user_id', String(36), ForeignKey('users.id')))

session_tags = Table('session_tags', database.Base.metadata,
                     Column('session_id', String(36),
                            ForeignKey('sessions.id')),
                     Column('tag_id', String(20), ForeignKey('tags.name')))


class User(database.Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    hashed_password = Column(String)
    fullname = Column(String)
    email = Column(String)


class Session(database.Base):
    __tablename__ = "sessions"

    id = Column(String(36), primary_key=True, index=True)
    name = Column(String, index=True)
    owner_id = Column(String(36), ForeignKey("users.id"))
    description = Column(String)

    owner = relationship("User", backref="owned_sessions")
    members = relationship("User",
                           secondary=session_members,
                           backref="sessions")
    tags = relationship("Tag",
                        secondary=session_tags,
                        backref="sessions")


class Image(database.Base):
    __tablename__ = "images"

    id = Column(String(36), primary_key=True, index=True)
    name = Column(String, index=True)
    owner_id = Column(String(36), ForeignKey("users.id"))
    session_id = Column(String(36), ForeignKey("sessions.id"))
    thumbnail = Column(String(36), ForeignKey("backend_objects.id"))
    raw = Column(String(36), ForeignKey("backend_objects.id"))
    preview = Column(String(36), ForeignKey("backend_objects.id"))
    image = Column(String(36), ForeignKey("backend_objects.id"))

    owner = relationship("User", backref="owned_images")
    session = relationship("Session", backref="images")
    tags = relationship("Tag",
                        secondary=image_tags,
                        backref="images")
    models = relationship("User",
                          secondary=image_models,
                          backref="modelled_images")


class ObjectData(database.Base):
    __tablename__ = "backend_objects"

    id = Column(String(36), primary_key=True, index=True)
    type = Column(String(20))
    backend = Column(String(36))
    uri = Column(String)


class Tag(database.Base):
    __tablename__ = "tags"

    name = Column(String(20), primary_key=True)
    description = Column(String)
