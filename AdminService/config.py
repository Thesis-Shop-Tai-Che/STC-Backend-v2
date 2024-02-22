import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "")
    POSTGRES_DATABASE: str = os.getenv("POSTGRES_DATABASE", "")

    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "")
    JWT_REFRESH_SECRET_KEY: str = os.getenv("JWT_REFRESH_SECRET_KEY", "")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "")
    
    MJ_APIKEY_PUBLIC: str = os.getenv("MJ_APIKEY_PUBLIC", "")
    MJ_APIKEY_PRIVATE: str = os.getenv("MJ_APIKEY_PRIVATE", "")

    class Config:
        env_file = "/.env"


settings = Settings()
