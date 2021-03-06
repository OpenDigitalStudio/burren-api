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
from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class MemberOwner(BaseModel):
    name: str
    id: str

    class Config:
        orm_mode = True


class ImageID(BaseModel):
    id: str
    name: str

    class Config:
        orm_mode = True


class SessionID(BaseModel):
    id: str
    name: str

    class Config:
        orm_mode = True


class TagBase(BaseModel):
    name: str
    description: str


class TagCreate(TagBase):
    pass


class Tag(TagBase):
    pass

    class Config:
        orm_mode = True


class ObjectType(str, Enum):
    image = "Image"


class ObjectDataBase(BaseModel):
    object_type: ObjectType = ObjectType.image


class ObjectDataCreate(ObjectDataBase):
    owner_id: str
    uri: Optional[str] = None


class ObjectData(ObjectDataBase):
    id: str
    owner: MemberOwner
    backend: Optional[str] = None

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str


class UserCreate(UserBase):
    password: str
    fullname: str
    email: str


class UserPassword(UserBase):
    id: str
    fullname: str
    email: str
    hashed_password: str

    class Config:
        orm_mode = True


class User(UserBase):
    id: str
    fullname: str
    email: str
    owned_images: List[ImageID] = None
    owned_sessions: List[SessionID] = None
    sessions: List[SessionID] = None

    class Config:
        orm_mode = True


class SessionBase(BaseModel):
    name: str
    description: Optional[str] = None


class SessionCreate(SessionBase):
    members: List[str] = []
    tags: List[str] = []


class Session(SessionBase):
    id: str
    owner: MemberOwner
    members: List[MemberOwner] = []
    tags: List[Tag]

    class Config:
        orm_mode = True


class ImageBase(BaseModel):
    name: str


class ImageCreate(ImageBase):
    session_id: Optional[str] = None
    model_ids: List[str] = []
    thumbnail: Optional[str] = None
    raw: Optional[str] = None
    preview: Optional[str] = None
    image_data: Optional[str] = None
    tags: List[str] = []


class Image(ImageBase):
    id: str
    owner: MemberOwner
    session: Optional[Session] = None
    thumbnail: Optional[ObjectData] = None
    raw: Optional[ObjectData] = None
    preview: Optional[ObjectData] = None
    image: Optional[ObjectData] = None
    tags: List[Tag] = []

    class Config:
        orm_mode = True


class TokenBase(BaseModel):
    id: str


class Token(TokenBase):
    created_at: datetime = None
    expires_at: datetime = None
    user_id: str

    class Config:
        orm_mode = True
