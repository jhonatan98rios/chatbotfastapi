from fastapi import APIRouter, HTTPException, status, Depends
from app.lib.database.mongo_db_connection import MongoDBConnection
from app.lib.entities.whatsapp_message import WhatsappMessage
from app.lib.mappers.context_mapper import context_to_json_mapper
from app.lib.providers.message_provider.twilio_message_provider import TwilioMessageProvider
from app.lib.repository.mongodb_repository import MongoDBRepository
from app.lib.services.chat_service import ChatService
from app.lib.providers.completion_provider.open_ai_completion_provider import OpenAiCompletionProvider
from pymongo.collection import Collection
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.lib.database.mongo_db_connection import mongodb_connection

router = APIRouter()


# Função para obter a conexão com o MongoDB
def get_mongo_connection() -> Collection:
    return mongodb_connection.get_collection()


# Definindo o ciclo de vida da aplicação com lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: inicializa a conexão com o MongoDB
    mongodb_connection.connect()
    print("MongoDB connected")
    
    # Deixe a aplicação rodar
    yield

    # Shutdown: fecha a conexão
    mongodb_connection.close()
    print("MongoDB connection closed")
    
    

@router.get("/health", status_code=status.HTTP_200_OK)
def health():
    try:
        get_mongo_connection()
    except Exception as ex:
        return {"status": status.HTTP_500_INTERNAL_SERVER_ERROR, "message": str(ex)}
    finally:
        return {"status": 200}



@router.post("/webhook")
def chat(message: WhatsappMessage, collection: Collection = Depends(get_mongo_connection)):
    
    if message.Body is None:
        raise HTTPException(status_code=400, detail="Empty message")

    # Initialize providers and repository
    completion_provider = OpenAiCompletionProvider()
    message_provider = TwilioMessageProvider()
    
    # Use the singleton connection
    repository = MongoDBRepository(collection)
    
    # Initialize the chat service
    chat_service = ChatService(
        repository=repository,
        completion_provider=completion_provider,
        message_provider=message_provider
    )
    
    try:
        response = chat_service.execute(message.From, message.Body)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return {"message_received": context_to_json_mapper(response)}
