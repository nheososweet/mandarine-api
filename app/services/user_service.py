from sqlalchemy.orm import Session
from app.models.user import User
from app.models.workspace import Workspace, WorkspaceMember, WorkspaceRole
from app.schemas.user import UserCreate
from app.core.security import get_password_hash

def create_user_with_default_workspace(db: Session, user_in: UserCreate):
    # 1. Tạo User
    user = User(
        email=user_in.email,
        password_hash=get_password_hash(user_in.password),
        full_name=user_in.full_name,
        is_active=True
    )
    db.add(user)
    db.flush() # Lấy user.id

    # 2. Tạo Workspace mặc định
    # Logic đặt tên: "Tan's Workspace"
    ws_name = f"{user_in.full_name.split()[0]}'s Workspace" if user_in.full_name else "My Workspace"
    
    workspace = Workspace(
        name=ws_name,
        owner_id=user.id
    )
    db.add(workspace)
    db.flush() # Lấy workspace.id

    # 3. Add User vào làm Admin
    member = WorkspaceMember(
        workspace_id=workspace.id,
        user_id=user.id,
        role=WorkspaceRole.ADMIN
    )
    db.add(member)

    db.commit()
    db.refresh(user)
    db.refresh(workspace)
    
    return user, workspace