from pydantic import BaseModel
from typing import Optional

class Completion(BaseModel):
    answer: str
    context: str
    product: Optional[str] = None
    quantity: Optional[int] = None
    followup: Optional[int] = None