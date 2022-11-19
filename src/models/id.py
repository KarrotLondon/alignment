from typing import Any, Generator

from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls) -> Generator[Any, ObjectId, Any]:
        yield cls.validate

    @classmethod
    def validate(cls, v: Any) -> ObjectId:
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema: Any) -> None:
        field_schema.update(type="string")
