from motor.motor_asyncio import AsyncIOMotorCollection
from typing import Optional, List
from app.lib.repository.abstract_repository import AbstractRepository
from app.lib.models.context_model import Context
from bson import ObjectId


class MongoDBRepository(AbstractRepository):
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection: AsyncIOMotorCollection = collection

    async def create_context(self, context: Context) -> Context:
        result = await self.collection.insert_one(context.dict(by_alias=True))
        context.id = result.inserted_id
        return context
    
    async def get_context(self, context_id: str) -> Optional[Context]:
        context_data = await self.collection.find_one({"_id": ObjectId(context_id)})
        if context_data:
            return Context(**context_data)
        
    async def get_context_by_phone_number(self, phone_number: str) -> Optional[Context]:
        context_data = await self.collection.find_one({"phone_number": phone_number})
        if context_data:
            return Context(**context_data)

    async def list_contexts(self) -> List[Context]:
        contexts_cursor = self.collection.find({})
        contexts = await contexts_cursor.to_list(length=100)
        return [Context(**context) for context in contexts]
    
    async def update_context(self, context_id: str, context: Context) -> Optional[Context]:
        await self.collection.update_one({"_id": ObjectId(context_id)}, {"$set": context.dict(exclude={"id"}, by_alias=True)})
        return await self.get_context(context_id)