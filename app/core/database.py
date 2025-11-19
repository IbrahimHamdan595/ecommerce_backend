from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.core.config import settings

# Global variables for client / db
client: AsyncIOMotorClient | None = None
db: AsyncIOMotorDatabase | None = None

async def connect_to_mongo() -> None:
	global client, db
	if client is None:
		client = AsyncIOMotorClient(settings.MONGODB_URI)
		db = client[settings.MONGODB_DB_NAME]
		print("MongoDB connected:", settings.MONGODB_DB_NAME)

async def close_mongo_connection() -> None:
	global client
	if client:
		client.close()
		print("MongoDB connection closed")