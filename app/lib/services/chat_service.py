from typing import Any
from app.lib.providers.completion_provider.abstract_completion_provider import AbstractCompletionProvider
from app.lib.providers.message_provider.abstract_message_provider import AbstractMessageProvider

class ChatService:

    __repository: Any
    __completion_provider: AbstractCompletionProvider
    __message_provider: AbstractMessageProvider

    def __init__(self, repository: Any, completion_provider: AbstractCompletionProvider, message_provider: AbstractMessageProvider):
        self.__repository = repository
        self.__completion_provider = completion_provider
        self.__message_provider = message_provider

    def execute(self, body: str):
        # Verificar se existe uma sessão com esse usuário
        # Se não, criar
        # Verificar se existe um contexto com esse usuário
        # Se não, criar
        # Enviar requisição para a API da Open AI com as instruções, a mensagem e o contexto.
        # Receber o resultado da Open AI
        # Tratar as estruturas e executar as lógicas necessárias

        # Responder ao usuário
        self.__message_provider.sendMessage(id="", to="", body="")
        return body
