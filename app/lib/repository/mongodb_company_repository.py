from pymongo.collection import Collection
from typing import Optional
from app.lib.repository.abstract_company_repository import AbstractCompanyRepository
from app.lib.models.company_model import Company
from bson import ObjectId


class MongoDBCompanyRepository(AbstractCompanyRepository):
    
    __slots__ = ['collection']
    
    def __init__(self, collection: Collection):
        self.collection: Collection = collection   
    
    def get_company_by_phone_number(self, phone_number: str) -> Optional[Company]:
        company_data = self.collection.find_one({"phone_number": phone_number})
        if company_data:
            return Company(**company_data)

    