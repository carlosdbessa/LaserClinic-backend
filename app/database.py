from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "laserclinic")

async def init_db(app_models: list):
    client = AsyncIOMotorClient(MONGODB_URL)
    await init_beanie(
        database=client[DB_NAME],
        document_models=app_models
    )