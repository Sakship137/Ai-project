import os
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional

class Database:
    client: Optional[AsyncIOMotorClient] = None
    database = None

db = Database()

async def get_database():
    return db.database

async def init_db():
    #Initialization 
    MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "smart_diet_db")
    
    try:
        db.client = AsyncIOMotorClient(MONGODB_URL)
        db.database = db.client[DATABASE_NAME]
        
        # Test connection
        await db.client.admin.command('ping')
        print("Successfully connected to MongoDB")
        
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        db.database = None

async def close_db():
    #Close database connection
    if db.client:
        db.client.close()
