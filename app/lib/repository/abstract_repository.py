from abc import abstractmethod
from typing import Optional, List
from app.lib.models.context_model import Context



class AbstractRepository:

    @abstractmethod
    async def create_context(self, context: Context) -> Context:
        pass
    
    @abstractmethod
    async def get_context(self, context_id: str) -> Optional[Context]:
        pass

    @abstractmethod
    async def get_context_by_phone_number(self, phone_number: str) -> Optional[Context]:
        pass

    @abstractmethod
    async def list_contexts(self) -> List[Context]:
        pass
    
    @abstractmethod
    async def update_context(self, context_id: str, context: Context) -> Optional[Context]:
        pass