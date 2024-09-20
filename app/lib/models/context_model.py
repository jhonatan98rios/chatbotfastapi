import uuid
from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId
from datetime import datetime, timezone


class PyObjectId(ObjectId):
    """To handle ObjectId conversion with Pydantic"""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class Message(BaseModel):
    id: Optional[str]
    author: str
    body: str


class Context(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    phone_number: str
    created_at: Optional[str] = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    messages: List[Message]
    
    @staticmethod
    def create(phone_number: str, body: str):
        message = Message(
            id=str(uuid.uuid4()),
            author=phone_number,
            body=body
        )

        context = Context(
            phone_number=phone_number,
            messages=[message]
        )

        return context

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        