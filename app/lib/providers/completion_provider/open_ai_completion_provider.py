from app.lib.providers.completion_provider.abstract_completion_provider import AbstractCompletionProvider

class OpenAiCompletionProvider(AbstractCompletionProvider):

    def __init__(self) -> None:
        pass

    def execute(self, message: str) -> str:
        return message
    