from datetime import datetime, timedelta
from typing import Any, Union
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

# Cấu hình thuật toán hash password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Cấu hình JWT (Lấy từ config)
# Lưu ý: Bạn nên check file app/core/config.py đã có SECRET_KEY chưa nhé
ALGORITHM = "HS256"

def create_access_token(
    subject: Union[str, Any], 
    workspace_id: str,  # 👈 Thêm tham số bắt buộc này
    expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {
        "exp": expire, 
        "sub": str(subject),
        "workspace_id": str(workspace_id) # ✅ Nhét ID vào payload
    }
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Kiểm tra mật khẩu nhập vào có khớp với hash trong DB không"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Băm mật khẩu ra chuỗi mã hóa"""
    return pwd_context.hash(password)

def create_invite_token(user_id: Union[str, Any], workspace_id: str) -> str:
    expire = datetime.utcnow() + timedelta(hours=24) # Link hết hạn sau 24h
    to_encode = {
        "exp": expire,
        "sub": str(user_id),           # Người được mời
        "workspace_id": str(workspace_id), # Mời vào workspace nào
        "type": "invite"               # Đánh dấu đây là token mời
    }
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt