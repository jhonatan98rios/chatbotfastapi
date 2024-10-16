
from abc import ABC, abstractmethod

from app.lib.entities.completion import Completion

class AbstractCompletionProvider(ABC):

    @abstractmethod
    def execute(self, message: str) -> Completion:
        pass