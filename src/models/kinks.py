from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, Field

from src.models.enums import Enjoyment, Experience, Frequency
from src.models.id import PyObjectId
from src.models.kink import Kink


class Kinks(BaseModel):
    sub: List[Kink]
    dom: List[Kink]
    
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "id": "hadasjda",
                "kink_name": "Jane Doe",
                "experience": "None",
                "frequency": "jdoe@example.com",
                "enjoyment": "gfdhgdhdgfsdsgsdfg"
            }
        }