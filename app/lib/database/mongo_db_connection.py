import os
from typing import Optional
from pymongo import MongoClient
from pymongo.collection import Collection

class MongoDBConnection:
    
    _instance: Optional["MongoDBConnection"] = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, 'initialized'):
            return
        
        db_url = os.getenv("CONNECTION_STRING")
        db_name = os.getenv("DB_NAME")

        if not db_url or not db_name:
            raise EnvironmentError("Environment variables for database connection are not set.")
        
        self.db_url = db_url
        self.db_name = db_name
        
        self.client = MongoClient(self.db_url)
        self.db = self.client[self.db_name]
        self.initialized = True
        
    def get_collection(self) -> Collection:
        return self.db["contexts"]  # type: ignore
    
    def close(self):
        if self.client is not None:
            self.client.close()
            self.client = None
            self.db = None
