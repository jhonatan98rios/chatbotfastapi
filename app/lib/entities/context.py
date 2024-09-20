from datetime import datetime
from typing import List
from pydantic import BaseModel
import uuid

class Message(BaseModel):
    id: str
    author: str
    body: str


class Context(BaseModel):
    id: str
    phone_number: str
    created_at: str
    messages: List[Message]