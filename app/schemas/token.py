from typing import Optional
from pydantic import BaseModel
from app.schemas.workspace import WorkspaceResponse # 👈 Import schema vừa tạo

class Token(BaseModel):
    access_token: str
    token_type: str
    current_workspace: WorkspaceResponse # 👈 Trả về nguyên Object cho FE hiển thị

class TokenPayload(BaseModel):
    sub: Optional[str] = None
    workspace_id: Optional[str] = None # 👈 Token ghi nhớ workspace ID