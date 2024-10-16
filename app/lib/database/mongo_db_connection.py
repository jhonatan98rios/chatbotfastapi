from contextlib import asynccontextmanager
import os
from typing import Optional
from pymongo import MongoClient
from pymongo.collection import Collection

from fastapi import FastAPI
from pymongo import MongoClient
import os

class MongoDBConnection:
    
    __slots__ = ['client', 'db']
    
    def connect(self):
        db_url = os.getenv("CONNECTION_STRING")
        db_name = os.getenv("DB_NAME")

        if not db_url or not db_name:
            raise EnvironmentError("Environment variables for database connection are not set.")
        
        self.client = MongoClient(db_url)
        self.db = self.client[db_name]

    def get_collection(self, collection_name: str = "contexts") -> Collection:
        return self.db[collection_name] # type: ignore

    def close(self):
        if self.client:
            self.client.close()


# Criação de uma instância Singleton
mongodb_connection = MongoDBConnection()


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