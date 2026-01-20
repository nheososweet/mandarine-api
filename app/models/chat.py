from sqlalchemy import Column, String, Text, ForeignKey, Enum, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.models.base_class import Base
import enum

class MessageRole(str, enum.Enum):
    USER = "USER"
    ASSISTANT = "ASSISTANT"
    SYSTEM = "SYSTEM"
    TOOL = "TOOL"

class ChatSession(Base):
    __tablename__ = "chat_sessions"

    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id", ondelete="CASCADE"))
    
    title = Column(String)

    user = relationship("User", back_populates="chat_sessions")
    # Thêm relationship với Workspace để truy vấn ngược nếu cần
    workspace = relationship("Workspace", back_populates="chat_sessions") 
    agent = relationship("Agent", back_populates="chat_sessions")
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    session_id = Column(UUID(as_uuid=True), ForeignKey("chat_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(Enum(MessageRole), nullable=False)
    content = Column(Text, nullable=True)
    
    tool_call_id = Column(String, nullable=True)
    tool_data = Column(JSONB, nullable=True)
    token_count = Column(Integer, default=0)

    session = relationship("ChatSession", back_populates="messages")