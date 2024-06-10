import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv('env/.env')


class Settings(BaseSettings):
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    GOOGLE_TOKEN_ENDPOINT: str = "https://oauth2.googleapis.com/token"
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET")
    REDIRECT_URI: str = "http://127.0.0.1:8000/auth/google"
    MONGO_DB_URI: str = os.getenv("MONGO_DB_URI")
    OPEN_API_KEY: str = os.getenv("OPEN_API_KEY")
    ASSISTANT_ID: str = os.getenv("ASSISTANT_ID")


settings = Settings()
