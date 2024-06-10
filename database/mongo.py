from fastapi import APIRouter
from motor.motor_asyncio import AsyncIOMotorClient

from settings import settings

router = APIRouter()


class MongoClient:
    _client: AsyncIOMotorClient = None

    @classmethod
    def get_client(cls):
        if not cls._client:
            cls._client = AsyncIOMotorClient(settings.MONGO_DB_URI)
        return cls._client


@router.on_event("startup")
async def startup_event():
    MongoClient.get_client()


@router.on_event("shutdown")
async def shutdown_event():
    mongodb_client = MongoClient.get_client()
    if mongodb_client:
        mongodb_client.close()
        print('successfully close mongo db client')
