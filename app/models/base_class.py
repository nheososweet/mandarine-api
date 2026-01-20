import uuid
from typing import Any
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

@as_declarative()
class Base:
    # --- ĐÃ XÓA 2 DÒNG GÂY LỖI: id: Any và __name__: str ---
    # SQLAlchemy tự động hiểu thông qua Column bên dưới rồi.

    # Tự động lấy tên Class làm tên bảng (viết thường + 's')
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"

    # ID UUID và CreatedAt tự động cho mọi bảng
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())