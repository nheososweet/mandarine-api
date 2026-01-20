from sqlalchemy.orm import Session
from uuid import UUID
from typing import Tuple, List

from app.models.workspace import Workspace, WorkspaceMember, WorkspaceRole
from app.schemas.workspace import WorkspaceCreate, WorkspaceUpdate

# 1. TẠO WORKSPACE (Logic cũ + chuẩn hóa)
def create_workspace(db: Session, workspace_in: WorkspaceCreate, owner_id: UUID) -> Workspace:
    # A. Tạo Workspace
    db_workspace = Workspace(
        name=workspace_in.name,
        description=workspace_in.description,
        icon_url=workspace_in.icon_url,
        owner_id=owner_id
    )
    db.add(db_workspace)
    db.flush() # Để lấy ID

    # B. Add Owner làm Admin
    member = WorkspaceMember(
        workspace_id=db_workspace.id,
        user_id=owner_id,
        role=WorkspaceRole.ADMIN
    )
    db.add(member)
    
    db.commit()
    db.refresh(db_workspace)
    return db_workspace

# 2. LẤY DANH SÁCH (Có Pagination)
def get_my_workspaces(
    db: Session, 
    user_id: UUID, 
    page: int, 
    size: int
) -> Tuple[List[Workspace], int]:
    """
    Trả về: (List[Workspace], total_count)
    """
    # Query cơ bản: Join bảng Member để chỉ lấy WS của mình
    query = (
        db.query(Workspace)
        .join(WorkspaceMember, Workspace.id == WorkspaceMember.workspace_id)
        .filter(WorkspaceMember.user_id == user_id)
    )

    # Đếm tổng số bản ghi (cho phân trang)
    total = query.count()

    # Phân trang (Offset / Limit)
    items = query.order_by(Workspace.created_at.desc())\
                 .offset((page - 1) * size)\
                 .limit(size)\
                 .all()
    
    return items, total

# 3. LẤY CHI TIẾT (Check quyền thành viên)
def get_workspace_by_id(db: Session, workspace_id: UUID, user_id: UUID) -> Workspace:
    # Check xem user có trong WS này không
    member = db.query(WorkspaceMember).filter(
        WorkspaceMember.workspace_id == workspace_id,
        WorkspaceMember.user_id == user_id
    ).first()
    
    if not member:
        return None
        
    return db.query(Workspace).filter(Workspace.id == workspace_id).first()

# 4. UPDATE WORKSPACE
def update_workspace(
    db: Session, 
    workspace_id: UUID, 
    workspace_in: WorkspaceUpdate, 
    user_id: UUID
) -> Workspace:
    # Check quyền (Phải là Admin mới được sửa - Tùy logic bạn)
    member = db.query(WorkspaceMember).filter(
        WorkspaceMember.workspace_id == workspace_id,
        WorkspaceMember.user_id == user_id,
        WorkspaceMember.role == WorkspaceRole.ADMIN # Chỉ Admin đc sửa
    ).first()
    
    if not member:
        return None # Hoặc raise exception ở tầng API

    workspace = db.query(Workspace).filter(Workspace.id == workspace_id).first()
    
    # Update các trường có gửi lên
    if workspace_in.name is not None:
        workspace.name = workspace_in.name
    if workspace_in.description is not None:
        workspace.description = workspace_in.description
    if workspace_in.icon_url is not None:
        workspace.icon_url = workspace_in.icon_url
        
    db.commit()
    db.refresh(workspace)
    return workspace

# 5. CHECK THÀNH VIÊN (Helper cho Invite)
def check_is_member(db: Session, workspace_id: UUID, user_id: UUID) -> bool:
    return db.query(WorkspaceMember).filter(
        WorkspaceMember.workspace_id == workspace_id,
        WorkspaceMember.user_id == user_id
    ).first() is not None

# 6. ADD MEMBER (Helper cho Invite)
def add_user_to_workspace(db: Session, workspace_id: UUID, user_id: UUID, role: WorkspaceRole):
    # Logic như cũ
    existing = db.query(WorkspaceMember).filter(
        WorkspaceMember.workspace_id == workspace_id,
        WorkspaceMember.user_id == user_id
    ).first()
    if existing: 
        return existing
        
    member = WorkspaceMember(workspace_id=workspace_id, user_id=user_id, role=role)
    db.add(member)
    db.commit()
    return member