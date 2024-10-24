
from abc import ABC, abstractmethod
from typing import Dict, List
from app.lib.models.context_model import Message

from app.lib.entities.completion import Completion

class AbstractCompletionProvider(ABC):

    @abstractmethod
    def execute(self, instructions: str, footer: str, messages: List[Message]) -> Completion:
        pass