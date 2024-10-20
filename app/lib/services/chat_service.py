import uuid
from app.lib.models.context_model import Context, Message
from app.lib.providers.completion_provider.abstract_completion_provider import AbstractCompletionProvider
from app.lib.providers.message_provider.abstract_message_provider import AbstractMessageProvider
from app.lib.repository.abstract_repository import AbstractRepository

class ChatService:
    
    __slots__ = ['__repository', '__completion_provider', '__message_provider']

    __repository: AbstractRepository
    __completion_provider: AbstractCompletionProvider
    __message_provider: AbstractMessageProvider

    def __init__(self, repository: AbstractRepository, completion_provider: AbstractCompletionProvider, message_provider: AbstractMessageProvider):
        self.__repository = repository
        self.__completion_provider = completion_provider
        self.__message_provider = message_provider

    def execute(self, phone_number: str, body: str):
        # Verificar se existe um contexto com esse usuário
        context = self.__repository.get_context_by_phone_number(phone_number)

        # Se não, criar
        if context is None:
            context = Context.create(phone_number=phone_number, role="user", content=body)
            self.__repository.create_context(context)
        else:
            message = Message(
                id=str(uuid.uuid4()), 
                role="user", 
                content=body
            )
            context.messages.append(message)
            
        print(context.dict())
        
        # Envia requisição para a API da Open AI com as instruções, a mensagem e o histórico.
        completion = self.__completion_provider.execute(context.messages)
        
        answer = Message(id=str(uuid.uuid4()), role="assistant", content=completion.answer)
        context.messages.append(answer)
        
        # Gravar no banco tanto a mensagem do usuário, quanto a completion
        self.__repository.update_context(context_id=str(context.id), context=context)       

        # Tratar as estruturas e executar as lógicas necessárias
        return completion

        # Responder ao usuário
        # self.__message_provider.sendMessage(id="", to="", body="")
        # return body
