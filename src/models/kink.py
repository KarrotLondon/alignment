from bson import ObjectId
from pydantic import BaseModel, Field
from src.models.enums import Frequency, Enjoyment, Experience
from typing import Optional

from src.models.id import PyObjectId

class Kink(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    kink_name: str
    experience: Optional[Experience] = None
    frequency: Optional[Frequency] = None
    enjoyment: Optional[Enjoyment] = None
    
    
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