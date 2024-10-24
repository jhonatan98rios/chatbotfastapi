from pydantic import BaseModel
from typing import Optional

class Completion(BaseModel):
    answer: str
    name: Optional[str] = None
    mail: Optional[str] = None
    address: Optional[str] = None
    product: Optional[str] = None
    quantity: Optional[int] = None
    #followup: Optional[int] = None