from fastapi import APIRouter, status
from app.lib.database.mongo_db_connection import MongoDBConnection
from app.lib.entities.whatsapp_message import WhatsappMessage
from app.lib.providers.message_provider.twilio_message_provider import TwilioMessageProvider
from app.lib.repository.mongodb_repository import MongoDBRepository
from app.lib.services.chat_service import ChatService
from app.lib.providers.completion_provider.open_ai_completion_provider import OpenAiCompletionProvider


router = APIRouter()

repository = MongoDBRepository(MongoDBConnection.get_connection())
completion_provider = OpenAiCompletionProvider()
message_provider = TwilioMessageProvider()
chat_service = ChatService(
    repository=repository,
    completion_provider=completion_provider,
    message_provider=message_provider
)

@router.get("/health", status_code=status.HTTP_200_OK)
async def health():
    return {"status": 200}


@router.post("/webhook")
async def chat(message: WhatsappMessage):
    
    if message.Body is None:
        return {"Empty message"}

    response = chat_service.execute(message.From, message.Body)
    return {"message_received": response}

