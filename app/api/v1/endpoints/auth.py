# from datetime import timedelta
# from typing import Any
# from fastapi import APIRouter, Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordRequestForm
# from sqlalchemy.orm import Session

# from app.api import deps
# from app.core import security
# from app.core.config import settings
# from app.models.user import User
# from app.schemas.token import Token
# from app.schemas.user import UserCreate, UserResponse

# router = APIRouter()

# # 1. API Đăng nhập (Login)
# @router.post("/login/access-token", response_model=Token)
# def login_access_token(
#     db: Session = Depends(deps.get_db),
#     form_data: OAuth2PasswordRequestForm = Depends()
# ) -> Any:
#     """
#     OAuth2 compatible token login, get an access token for future requests
#     """
#     # Tìm user trong DB (form_data.username chính là email gửi lên)
#     user = db.query(User).filter(User.email == form_data.username).first()
    
#     # Kiểm tra user và mật khẩu
#     if not user or not security.verify_password(form_data.password, user.password_hash):
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Incorrect email or password",
#         )
    
#     if not user.is_active:
#         raise HTTPException(status_code=400, detail="Inactive user")

#     # Tạo JWT Token
#     access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#     return {
#         "access_token": security.create_access_token(
#             user.id, expires_delta=access_token_expires
#         ),
#         "token_type": "bearer",
#     }

# # 2. API Đăng ký (Sign up)
# @router.post("/signup", response_model=UserResponse)
# def create_user_signup(
#     *,
#     db: Session = Depends(deps.get_db),
#     user_in: UserCreate,
# ) -> Any:
#     # Check trùng email
#     user = db.query(User).filter(User.email == user_in.email).first()
#     if user:
#         raise HTTPException(
#             status_code=400,
#             detail="The user with this email already exists in the system",
#         )
    
#     # Tạo user mới
#     user = User(
#         email=user_in.email,
#         # 👇 ĐÂY LÀ CHỖ GÂY LỖI: Phải chắc chắn có .password
#         password_hash=security.get_password_hash(user_in.password), 
#         full_name=user_in.full_name,
#         is_active=True
#     )
#     db.add(user)
#     db.commit()
#     db.refresh(user)
#     return user


from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from uuid import UUID

from app.api import deps
from app.core import security
from app.core.config import settings
from app.models.user import User
from app.models.workspace import WorkspaceMember, Workspace
from app.schemas.token import Token
from app.schemas.user import UserCreate
from app.services import user_service

router = APIRouter()

# --- 1. LOGIN ---
@router.post("/login/access-token", response_model=Token)
def login_access_token(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    # A. Xác thực User
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not security.verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    # B. Tìm Workspace mặc định (Cái đầu tiên tham gia)
    member = db.query(WorkspaceMember).filter(WorkspaceMember.user_id == user.id).first()
    if not member:
        raise HTTPException(status_code=400, detail="User has no workspace assigned")

    # C. Lấy thông tin chi tiết Workspace để trả về FE
    workspace = db.query(Workspace).filter(Workspace.id == member.workspace_id).first()

    # D. Tạo Token kèm Workspace ID
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            subject=user.id,
            workspace_id=member.workspace_id, # Context
            expires_delta=access_token_expires
        ),
        "token_type": "bearer",
        "current_workspace": workspace # Data cho FE
    }

# --- 2. SIGNUP ---
@router.post("/signup", response_model=Token)
def create_user_signup(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserCreate,
) -> Any:
    # A. Check Email
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    # B. Tạo User + Default Workspace
    user, workspace = user_service.create_user_with_default_workspace(db, user_in)
    
    # C. Login luôn (Trả Token)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            subject=user.id,
            workspace_id=workspace.id, # Context
            expires_delta=access_token_expires
        ),
        "token_type": "bearer",
        "current_workspace": workspace # Data cho FE
    }

# --- 3. SWITCH WORKSPACE ---
@router.post("/switch-workspace/{workspace_id}", response_model=Token)
def switch_workspace(
    workspace_id: UUID,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Đổi Workspace -> Cấp Token mới
    """
    # A. Kiểm tra quyền thành viên
    member = db.query(WorkspaceMember).filter(
        WorkspaceMember.user_id == current_user.id,
        WorkspaceMember.workspace_id == workspace_id
    ).first()
    
    if not member:
        raise HTTPException(status_code=403, detail="You are not a member of this workspace")

    # B. Lấy Info Workspace mới
    workspace = db.query(Workspace).filter(Workspace.id == workspace_id).first()
        
    # C. Cấp Token Mới
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            subject=current_user.id,
            workspace_id=workspace_id, # ID Mới
            expires_delta=access_token_expires
        ),
        "token_type": "bearer",
        "current_workspace": workspace # Object Mới
    }