from abc import ABC, abstractmethod


class AbstractQueueProvider(ABC):

    @abstractmethod
    def publish(self, message_body: str, message_attributes=None):
        pass