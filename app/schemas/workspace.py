from typing import Optional, List
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

# Import cái PagedResponse vừa tạo
from app.schemas.pagination import PagedResponse

# 1. Base
class WorkspaceBase(BaseModel):
    name: str
    description: Optional[str] = None
    icon_url: Optional[str] = None

# 2. Create (Client gửi lên)
class WorkspaceCreate(WorkspaceBase):
    pass

# 3. Update (Client gửi lên để sửa)
class WorkspaceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    icon_url: Optional[str] = None

# 4. Response (Trả về Client - 1 item)
class WorkspaceResponse(WorkspaceBase):
    id: UUID
    owner_id: UUID
    created_at: datetime
    # Có thể thêm trường này nếu muốn biết role của user hiện tại trong WS đó
    # my_role: Optional[str] = None 
    
    class Config:
        from_attributes = True

# 5. Response List (Trả về Client - Danh sách có phân trang)
# Cái này định nghĩa kiểu dữ liệu cho Swagger hiểu
class WorkspacePagedResponse(PagedResponse[WorkspaceResponse]):
    pass