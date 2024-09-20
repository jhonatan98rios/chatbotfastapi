from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

class MongoDBConnection:
    def __init__(self, db_url: str, db_name: str):
        self.db_url = db_url
        self.db_name = db_name
        self.client = None
        self.db = None

    def connect(self):
        self.client = AsyncIOMotorClient(self.db_url)
        self.db = self.client[self.db_name]

    def get_database(self):
        if self.db is None:
            raise ConnectionError("Database not connected. Call 'connect()' first.")
        return self.db

    def close(self):
        if self.client is not None:
            self.client.close()

    @staticmethod
    def get_connection() -> AsyncIOMotorCollection:
        db_url = "mongodb://localhost:27017"
        db_name = "mydatabase"
        db_connection = MongoDBConnection(db_url, db_name)
        db_connection.connect()
        return db_connection.get_database()["contexts"]