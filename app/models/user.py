from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship
from app.models.base_class import Base

class User(Base):
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=True)
    full_name = Column(String, index=True)
    avatar_url = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

    # Relationships
    owned_workspaces = relationship("Workspace", back_populates="owner")
    memberships = relationship("WorkspaceMember", back_populates="user")
    chat_sessions = relationship("ChatSession", back_populates="user")