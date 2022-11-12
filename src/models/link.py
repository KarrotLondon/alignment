from bson import ObjectId
from pydantic import BaseModel, Field
from typing import List
from src.models.enums import Roles
from src.models.kink import Kink

from src.models.id import PyObjectId

class Link(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: str | None = None
    username: str
    pending: bool
    mutual_required: bool
    requested: bool
    relationships: List[Roles]
    
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