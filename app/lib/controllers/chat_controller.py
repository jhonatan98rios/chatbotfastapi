from fastapi import APIRouter

from app.lib.entities.whats_app_message import WhatsAppMessage
from app.lib.providers.message_provider.twilio_message_provider import TwilioMessageProvider
from app.lib.services.chat_service import ChatService
from app.lib.providers.completion_provider.open_ai_completion_provider import OpenAiCompletionProvider

router = APIRouter()

@router.get("/webhook")
async def chat(message: WhatsAppMessage):
    
    if message.Body is None:
        return {"Empty message"}

    repository = ""
    completion_provider = OpenAiCompletionProvider()
    message_provider = TwilioMessageProvider()
    
    chat_service = ChatService(
        repository=repository,
        completion_provider=completion_provider,
        message_provider=message_provider
    )

    response = chat_service.execute(message.Body)
    return {"message_received": response}

