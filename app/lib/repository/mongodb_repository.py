from pymongo.collection import Collection
from typing import Optional
from app.lib.repository.abstract_repository import AbstractRepository
from app.lib.models.context_model import Context
from bson import ObjectId


class MongoDBRepository(AbstractRepository):
    def __init__(self, collection: Collection):
        self.collection: Collection = collection

    def create_context(self, context: Context) -> Context:
        result = self.collection.insert_one(context.dict(by_alias=True))
        context.id = result.inserted_id
        return context
    
    def get_context_by_phone_number(self, phone_number: str) -> Optional[Context]:
        context_data = self.collection.find_one({"phone_number": phone_number})
        if context_data:
            return Context(**context_data)

    def update_context(self, context_id: str, context: Context) -> Optional[Context]:
        self.collection.update_one(
            {"_id": ObjectId(context_id)}, 
            {"$set": context.dict(exclude={"id"}, by_alias=True)}
        )
        return self.get_context(context_id)
    
    def get_context(self, context_id: str) -> Optional[Context]:
        context_data = self.collection.find_one({"_id": ObjectId(context_id)})
        if context_data:
            return Context(**context_data)
