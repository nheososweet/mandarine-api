from sqlalchemy import Column, String, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base_class import Base
import enum

class WorkspaceRole(str, enum.Enum):
    ADMIN = "ADMIN"
    EDITOR = "EDITOR"
    VIEWER = "VIEWER"

class Workspace(Base):
    name = Column(String, nullable=False)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="owned_workspaces")
    members = relationship("WorkspaceMember", back_populates="workspace", cascade="all, delete-orphan")
    
    # Cascade delete: Xóa Workspace là xóa sạch dữ liệu con
    files = relationship("File", back_populates="workspace", cascade="all, delete-orphan")
    knowledge_bases = relationship("KnowledgeBase", back_populates="workspace", cascade="all, delete-orphan")
    agents = relationship("Agent", back_populates="workspace", cascade="all, delete-orphan")
    # Thêm relationship ngược cho chat
    chat_sessions = relationship("ChatSession", back_populates="workspace", cascade="all, delete-orphan")


class WorkspaceMember(Base):
    # Bảng trung gian User <-> Workspace
    __tablename__ = "workspace_members"
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    role = Column(Enum(WorkspaceRole, name="workspace_role"), default=WorkspaceRole.VIEWER)
    workspace = relationship("Workspace", back_populates="members")
    user = relationship("User", back_populates="memberships")