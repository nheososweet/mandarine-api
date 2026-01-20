# app/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Tạo engine kết nối
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True, # Tự động check kết nối sống/chết
    echo=False          # Set True nếu muốn in câu lệnh SQL ra terminal để debug
)

# Tạo SessionLocal để dùng trong các API
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)