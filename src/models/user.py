from typing import List, Optional

from bson import ObjectId
from flask_login import UserMixin
from pydantic import BaseModel, Field

from src.models.id import PyObjectId
from src.models.kink import Kink
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
                "password": "gfdhgdhdgfsdsgsdfg",
            }
        }

    def get_kinks_for_role(self, role: Optional[str]) -> List[Kink]:
        if not role:
            raise NotImplementedError
        kinks = self.kinks.sub if role == "sub" else self.kinks.dom
        return sorted(kinks, key=lambda x: x.kink_name.lower())
