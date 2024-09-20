from datetime import datetime
from app.lib.models.context_model import Context
from app.lib.providers.completion_provider.abstract_completion_provider import AbstractCompletionProvider
from app.lib.providers.message_provider.abstract_message_provider import AbstractMessageProvider
from app.lib.repository.abstract_repository import AbstractRepository

class ChatService:

    __repository: AbstractRepository
    __completion_provider: AbstractCompletionProvider
    __message_provider: AbstractMessageProvider

    def __init__(self, repository: AbstractRepository, completion_provider: AbstractCompletionProvider, message_provider: AbstractMessageProvider):
        self.__repository = repository
        self.__completion_provider = completion_provider
        self.__message_provider = message_provider

    async def execute(self, phone_number: str, body: str):
        # Verificar se existe um contexto com esse usuário
        context = await self.__repository.get_context_by_phone_number(phone_number)

        # Se não, criar
        if context is None:
            context = Context.create(phone_number, body)
            await self.__repository.create_context(context)

        # Enviar requisição para a API da Open AI com as instruções, a mensagem e o contexto.
        # Receber o resultado da Open AI
        # Tratar as estruturas e executar as lógicas necessárias

        # Responder ao usuário
        self.__message_provider.sendMessage(id="", to="", body="")
        return body
