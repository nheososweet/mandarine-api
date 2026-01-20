# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Mandarine API"
    API_V1_STR: str = "/api/v1"
    
    # Tự động đọc DATABASE_URL từ file .env
    DATABASE_URL: str

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()