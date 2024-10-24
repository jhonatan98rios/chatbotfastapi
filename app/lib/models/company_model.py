import uuid
from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId
from datetime import datetime, timezone
from enum import IntEnum

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
        
    
class Status(IntEnum):
    inactive = 0
    active = 1
    testing = 2
    
    
class Company(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    company_phone_number: str
    status: Status
    created_at: Optional[str] = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    instructions: str
    footer: str

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}