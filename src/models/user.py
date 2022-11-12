from typing import List

from bson import ObjectId
from flask_login import UserMixin
from pydantic import BaseModel, Field

from src.models.id import PyObjectId
from src.models.kinks import Kinks
from src.models.link import Link


class User(UserMixin, BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    email: str | None = None
    username: str
    password: str
    kinks: Kinks
    links: List[Link] = []
    
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "id": "hadasjda",
                "username": "Jane Doe",
                "email": "jdoe@example.com",
                "password": "gfdhgdhdgfsdsgsdfg"
            }
        }