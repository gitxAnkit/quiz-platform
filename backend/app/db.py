from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from typing import List
from models import User, Quiz  # Replace with the actual import paths of your models

class MongoDB:
    client: AsyncIOMotorClient = None

    @staticmethod
    async def connect(uri: str = "mongodb://localhost:27017", db_name: str = "quiz_platform"):
        """
        Connect to the MongoDB server and initialize Beanie with models.
        """
        # Connect the Motor client
        MongoDB.client = AsyncIOMotorClient(uri)
        print("Connected to MongoDB")

        # Initialize Beanie
        await init_beanie(database=MongoDB.client[db_name], document_models=[User, Quiz])
        print("Beanie initialized with database:", db_name)

    @staticmethod
    async def close():
        """
        Close the MongoDB connection.
        """
        if MongoDB.client:
            MongoDB.client.close()
            print("MongoDB connection closed")

db = MongoDB()
