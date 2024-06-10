from typing import Optional, List

from bson import ObjectId
from pydantic import BaseModel, Field

from database.models.object import ObjectIdPydanticAnnotation


class Message(BaseModel):
    role: str
    text: str
    file_id: str


class Thread(BaseModel):
    thread_id: str
    messages: List[Message] = []


class Users(BaseModel):
    id: Optional[ObjectIdPydanticAnnotation] = Field(default_factory=ObjectId, alias='_id')
    name: str
    email: str
    hashed_password: str
    threads: List[Thread]

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: lambda oid: str(oid)}
        from_attributes = True
