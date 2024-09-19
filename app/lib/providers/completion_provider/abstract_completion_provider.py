
from abc import ABC, abstractmethod

class AbstractCompletionProvider(ABC):

    @abstractmethod
    def execute(self, message: str) -> str:
        pass