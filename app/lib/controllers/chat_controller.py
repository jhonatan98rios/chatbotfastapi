from fastapi import APIRouter, status, Depends
from app.lib.entities.whatsapp_message import WhatsappMessage
from app.lib.errors.bad_request import BadRequestException
from app.lib.mappers.context_mapper import context_to_json_mapper
from app.lib.providers.message_provider.twilio_message_provider import TwilioMessageProvider
from app.lib.providers.queue_provider.sqs_queue_provider import SQSQueueProvider
from app.lib.repository.mongodb_repository import MongoDBRepository
from app.lib.repository.mongodb_company_repository import MongoDBCompanyRepository
from app.lib.services.chat_service import ChatService
from app.lib.providers.completion_provider.open_ai_completion_provider import OpenAiCompletionProvider
from pymongo.collection import Collection
from app.lib.database.mongo_db_connection import mongodb_connection
from app.lib.errors.internal_server_error import InternalServerErrorException

router = APIRouter()


# Função para obter a conexão com o MongoDB
def get_context_connection() -> Collection:
    return mongodb_connection.get_collection("contexts")

# Função para obter a conexão com o MongoDB
def get_company_connection() -> Collection:
    return mongodb_connection.get_collection("companies")
    

@router.get("/health", status_code=status.HTTP_200_OK)
def health():
    try:
        get_context_connection()
        return {"status": 200}
    except Exception as ex:
        return {"status": status.HTTP_500_INTERNAL_SERVER_ERROR, "message": str(ex)}


@router.post("/webhook")
def chat(message: WhatsappMessage, contexts: Collection = Depends(get_context_connection), companies: Collection = Depends(get_context_connection)):
    
    if message.Body is None:
        raise BadRequestException(detail="Empty message")

    # Initialize providers and repository
    completion_provider = OpenAiCompletionProvider()
    message_provider = TwilioMessageProvider()
    queue_provider = SQSQueueProvider()
    context_repository = MongoDBRepository(contexts)
    company_repository = MongoDBCompanyRepository(companies)
    
    # Initialize the chat service
    chat_service = ChatService(
        context_repository=context_repository,
        company_repository=company_repository,
        completion_provider=completion_provider,
        message_provider=message_provider,
        queue_provider=queue_provider
    )
    
    try:
        response = chat_service.execute(
            phone_number=message.From,
            company_phone_number=message.To,
            body=message.Body
        )
        return {"message_received": context_to_json_mapper(response)}
    
    except Exception as e:
        print(e)
        raise InternalServerErrorException(detail=str(e))
    
