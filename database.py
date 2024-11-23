from motor.motor_asyncio import AsyncIOMotorClient
from config import settings

# Inicializa o cliente do MongoDB
client = AsyncIOMotorClient(settings.mongodb_url)
database = client[settings.MONGODB_DATABASE]