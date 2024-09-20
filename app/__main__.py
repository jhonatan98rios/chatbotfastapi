from fastapi import FastAPI
from app.lib.database.mongo_db_connection import MongoDBConnection
from lib.controllers.chat_controller import router

app = FastAPI()
app.include_router(router)