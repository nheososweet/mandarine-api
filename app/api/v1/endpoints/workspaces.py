from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import EmailStr, BaseModel
from uuid import UUID
import math
from app.utils.email import send_invite_email # 👈 Import hàm gửi mail vừa viết
from app.core.config import settings
from app.api import deps
from app.models.user import User
# Import Schemas
from app.schemas.workspace import (
    WorkspaceCreate, 
    WorkspaceUpdate, 
    WorkspaceResponse, 
    WorkspacePagedResponse
)
from jose import jwt
from app.schemas.pagination import PageParams
from app.services import workspace_service

router = APIRouter()

# 1. GET LIST (Với Pagination Chuẩn)
@router.get("/", response_model=WorkspacePagedResponse)
def read_workspaces(
    page_params: PageParams = Depends(), # Tự động lấy ?page=1&size=10
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Lấy danh sách workspace của user (có phân trang)
    """
    items, total = workspace_service.get_my_workspaces(
        db, 
        user_id=current_user.id, 
        page=page_params.page, 
        size=page_params.size
    )
    
    # Tính toán tổng số trang
    total_pages = math.ceil(total / page_params.size) if page_params.size > 0 else 0
    
    return {
        "items": items,
        "total": total,
        "page": page_params.page,
        "size": page_params.size,
        "pages": total_pages
    }

# 2. CREATE
@router.post("/", response_model=WorkspaceResponse)
def create_workspace(
    *,
    db: Session = Depends(deps.get_db),
    workspace_in: WorkspaceCreate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    return workspace_service.create_workspace(
        db=db, 
        workspace_in=workspace_in, 
        owner_id=current_user.id
    )

# 3. GET DETAIL
@router.get("/{workspace_id}", response_model=WorkspaceResponse)
def read_workspace(
    workspace_id: UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    workspace = workspace_service.get_workspace_by_id(db, workspace_id, current_user.id)
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found or access denied")
    return workspace

# 4. UPDATE
@router.put("/{workspace_id}", response_model=WorkspaceResponse)
def update_workspace(
    workspace_id: UUID,
    workspace_in: WorkspaceUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    workspace = workspace_service.update_workspace(
        db, workspace_id, workspace_in, current_user.id
    )
    if not workspace:
        raise HTTPException(
            status_code=403, 
            detail="Cannot update: Workspace not found or you are not Admin"
        )
    return workspace

class InviteRequest(BaseModel):
    email: EmailStr

# 1. API GỬI LỜI MỜI (Có gửi mail thật)
@router.post("/invite", status_code=200)
async def invite_member( # 👈 Nhớ thêm async vì gửi mail là bất đồng bộ
    *,
    db: Session = Depends(deps.get_db),
    invite_in: InviteRequest,
    current_workspace_id: UUID = Depends(deps.get_current_workspace_id),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Gửi email invite user vào workspace hiện tại.
    """
    # A. Check user tồn tại
    target_user = db.query(User).filter(User.email == invite_in.email).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="Email không tồn tại trong hệ thống")

    # B. Check đã là thành viên chưa (Dùng service check cho gọn)
    if workspace_service.check_is_member(db, current_workspace_id, target_user.id):
        raise HTTPException(status_code=400, detail="User này đã là thành viên rồi")

    # C. Lấy thông tin Workspace (để hiển thị tên trong mail)
    workspace = workspace_service.get_workspace_by_id(db, current_workspace_id, current_user.id)

    # D. Tạo Link Invite
    # Token chứa: ID người được mời + ID workspace
    invite_token = security.create_invite_token(user_id=target_user.id, workspace_id=current_workspace_id)
    
    # Link trỏ về API Join (hoặc trang Frontend xử lý join)
    # Ví dụ: http://localhost:8000/api/v1/workspaces/join?token=...
    invite_link = f"{settings.SERVER_HOST}{settings.API_V1_STR}/workspaces/join?token={invite_token}"

    # E. Gửi Email thật 🚀
    try:
        await send_invite_email(
            email_to=target_user.email,
            workspace_name=workspace.name,
            invite_link=invite_link
        )
    except Exception as e:
        print(f"❌ Lỗi gửi mail: {e}")
        raise HTTPException(status_code=500, detail="Không thể gửi email mời")

    return {"message": f"Đã gửi lời mời tới {invite_in.email}"}


# 2. API JOIN (Xử lý khi user click link)
@router.get("/join")
def join_workspace(
    token: str,
    db: Session = Depends(deps.get_db)
):
    try:
        # A. Giải mã token
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[security.ALGORITHM])
        
        if payload.get("type") != "invite":
            raise HTTPException(status_code=400, detail="Token không hợp lệ")

        user_id = UUID(payload.get("sub"))
        workspace_id = UUID(payload.get("workspace_id"))

        # B. Thêm user vào workspace
        workspace_service.add_user_to_workspace(
            db=db,
            workspace_id=workspace_id,
            user_id=user_id,
            role=WorkspaceRole.VIEWER # Mặc định là Viewer
        )

        return {"message": "Chúc mừng! Bạn đã tham gia workspace thành công."}
        
    except (jwt.JWTError, jwt.ExpiredSignatureError):
        raise HTTPException(status_code=400, detail="Link mời đã hết hạn hoặc không hợp lệ")