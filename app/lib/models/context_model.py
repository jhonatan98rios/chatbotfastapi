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
    def validate(cls, v, field=None):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")



class Message(BaseModel):
    id: Optional[str]
    role: str
    content: str


class Context(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    phone_number: str
    created_at: Optional[str] = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    messages: List[Message]
    
    @staticmethod
    def create(phone_number:str, role: str, content: str):
        message = Message(
            id=str(uuid.uuid4()),
            role=role,
            content=content
        )

        context = Context(
            phone_number=phone_number,
            messages=[message]
        )

        return context

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        