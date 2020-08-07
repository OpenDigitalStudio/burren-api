from fastapi import FastAPI

from dsc.api.v1.routers import images
from dsc.api.v1.routers import items
from dsc.api.v1.routers import sessions
from dsc.api.v1.routers import users
from dsc.api.v1.routers import tags
from dsc.db import database
from dsc.userauth import oauth2

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(
        images.router,
        prefix='/v1/images',
        tags=['images'])
app.include_router(
        items.router,
        prefix='/v1/items',
        tags=['items'])
app.include_router(
        sessions.router,
        prefix='/v1/sessions',
        tags=['sessions'])
app.include_router(
        users.router,
        prefix='/v1/users',
        tags=['users'])
app.include_router(
        tags.router,
        prefix='/v1/tags',
        tags=['tags'])
app.include_router(
        oauth2.router,
        prefix='/userauth',
        tags=['auth'])
