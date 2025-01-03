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
    EXAMPLE_ASSISTANT_ID: str = os.getenv("EXAMPLE_ASSISTANT_ID")
    ASSISTANT_ID: str = os.getenv("ASSISTANT_ID")
    DATASET_INFO: dict = {"life": """This dataset provides aggregated life expectancy data averaged over multiple years 
    for various countries, along with associated socio-economic and health-related factors. It aims to facilitate 
    analysis of global health trends, the relationship between life expectancy and development indicators, 
    and regional disparities.""", "houses": """This dataset contains various characteristics and price information about 
    houses in London. Consisting of 1000 entries, it reflects many aspects of each house, from location to interior 
    design. In addition to physical features such as the address, neighborhood, number of rooms, and square footage, 
    it also includes more specific details like the age of the building, garage availability, and balcony presence. 
    Furthermore, the price of each house provides valuable insights into its market value.""", "shopping": """The 
    dataset offers a comprehensive view of consumer shopping trends, aiming to uncover patterns and behaviors in 
    retail purchasing. It contains detailed transactional data across various product categories, 
    customer demographics, and purchase channels."""}


settings = Settings()
