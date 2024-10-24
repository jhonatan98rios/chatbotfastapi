import uuid
import json

from app.lib.entities.completion import Completion
from app.lib.models.context_model import Context, Message

from app.lib.providers.completion_provider.abstract_completion_provider import AbstractCompletionProvider
from app.lib.providers.message_provider.abstract_message_provider import AbstractMessageProvider
from app.lib.providers.queue_provider.abstract_queue_provider import AbstractQueueProvider

from app.lib.repository.abstract_repository import AbstractRepository
from app.lib.repository.abstract_company_repository import AbstractCompanyRepository

class ChatService:
    
    __slots__ = ['__context_repository', '__company_repository', '__completion_provider', '__message_provider', '__queue_provider']

    __context_repository: AbstractRepository
    __company_repository: AbstractCompanyRepository
    __completion_provider: AbstractCompletionProvider
    __message_provider: AbstractMessageProvider
    __queue_provider: AbstractQueueProvider

    def __init__(
        self, 
        context_repository: AbstractRepository, 
        company_repository: AbstractCompanyRepository,
        completion_provider: AbstractCompletionProvider, 
        message_provider: AbstractMessageProvider, 
        queue_provider: AbstractQueueProvider
    ):
        self.__context_repository = context_repository
        self.__company_repository = company_repository
        self.__completion_provider = completion_provider
        self.__message_provider = message_provider
        self.__queue_provider = queue_provider
        

    def execute(self, phone_number: str, company_phone_number: str, body: str):
        # Recupera o contexto para aquela conversa, caso exista e caso não, cria um novo
        context = self.get_or_create_context(
            client_phone_number=phone_number,
            company_phone_number=company_phone_number,
            body=body
        )
        
        # Envia requisição para a API da Open AI com as instruções, a mensagem e o histórico.
        completion = self.__completion_provider.execute(
            instructions=context.instructions, 
            footer=context.footer, 
            messages=context.messages
        )
        
        answer = Message(id=str(uuid.uuid4()), role="assistant", content=completion.answer)
        context.messages.append(answer)
        
        # Gravar no banco tanto a mensagem do usuário, quanto a completion
        self.__context_repository.update_context(context_id=str(context.id), context=context)
        
        # Lidar com os casos de uso específicos
        self.handle_use_cases(phone_number, completion)

        # Tratar as estruturas e executar as lógicas necessárias
        return completion

        # Responder ao usuário
        # self.__message_provider.sendMessage(id="", to="", body="")
        # return body


    def get_or_create_context(self, client_phone_number: str, company_phone_number: str,  body: str):
        # Verificar se existe um contexto com esse usuário
        context = self.__context_repository.get_context_by_phone_number(client_phone_number)

        # Se não, criar
        if context is None:
            
            company = self.__company_repository.get_company_by_phone_number(company_phone_number)
            
            context = Context.create(
                phone_number=client_phone_number,
                company_phone_number=company_phone_number,
                role="user",
                content=body,
                instructions=company.instructions,
                footer=company.footer
            )
            
            self.__context_repository.create_context(context)
        else:
            message = Message(
                id=str(uuid.uuid4()), 
                role="user",
                content=body
            )
            context.messages.append(message)
            
        print(context.dict())
        return context
    
    
    def handle_use_cases(self, client_phone_number: str, completion: Completion):
        if completion.product is not None and completion.quantity is not None and completion.name is not None and completion.mail is not None and completion.address is not None:
        
            message_attributes = {
                "EventType": {
                    'StringValue': 'Service Order',
                    'DataType': 'String'
                }
            }
        
            body = {
                "phone_number": client_phone_number,
                "name": completion.name,
                "mail": completion.mail,
                "address": completion.address,
                "product": completion.product,
                "quantity": completion.quantity,
            }
            
            self.__queue_provider.publish(json.dumps(body), message_attributes)
        
        # if completion.followup is not None:
        #     message_attributes = {
        #         "EventType": {
        #             'StringValue': 'Follow Up',
        #             'DataType': 'String'
        #         }
        #     }
        
        #     body = {
        #         "phone_number": phone_number
        #     }
            
        #     self.__queue_provider.publish(json.dumps(body), message_attributes)
