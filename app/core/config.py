# app/core/config.py
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Mandarine API"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str
    
    # 👇 THÊM CÁC DÒNG NÀY 👇
    # Security (Nên đổi chuỗi này thành một chuỗi ngẫu nhiên dài)
    SECRET_KEY: str = "YOUR_SUPER_SECRET_KEY_CHANGE_IT_IN_ENV_FILE"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8 # 8 ngày

    # CẤU HÌNH EMAIL (Thêm mới)
    MAIL_USERNAME: str = "your_email@gmail.com"
    MAIL_PASSWORD: str = "your_app_password" # Mật khẩu ứng dụng (không phải pass đăng nhập)
    MAIL_FROM: str = "your_email@gmail.com"
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True
    
    # URL của Backend (để tạo link join)
    SERVER_HOST: str = "http://localhost:8000"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()