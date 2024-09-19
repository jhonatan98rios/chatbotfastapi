from abc import ABC, abstractmethod


class AbstractMessageProvider(ABC):

    @abstractmethod
    def sendMessage(self, id: str, to: str, body: str):
        pass