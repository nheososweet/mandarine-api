from typing import Optional
from pydantic import BaseModel, EmailStr
from uuid import UUID

# Các trường chung
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    is_active: Optional[bool] = True

# Dùng khi User Đăng ký (Client gửi lên)
class UserCreate(UserBase):
    password: str

# Dùng khi Update thông tin
class UserUpdate(UserBase):
    password: Optional[str] = None
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None

# Dùng để trả về cho Client (Giấu mật khẩu đi)
class UserResponse(UserBase):
    id: UUID
    avatar_url: Optional[str] = None
    
    class Config:
        from_attributes = True