from sqlalchemy import Column, String, Integer, ForeignKey, Enum, Text, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base_class import Base
import enum

class FileStatus(str, enum.Enum):
    UPLOADING = "UPLOADING"
    PROCESSING = "PROCESSING"
    READY = "READY"
    ERROR = "ERROR"

# Bảng liên kết N-N: Knowledge <-> File
knowledge_file_link = Table(
    "knowledge_files",
    Base.metadata,
    Column("knowledge_id", UUID(as_uuid=True), ForeignKey("knowledge_bases.id", ondelete="CASCADE"), primary_key=True),
    Column("file_id", UUID(as_uuid=True), ForeignKey("files.id", ondelete="CASCADE"), primary_key=True)
)

class File(Base):
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False)
    uploader_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    
    name = Column(String, nullable=False)
    storage_path = Column(String, nullable=False)
    mime_type = Column(String)
    size = Column(Integer)
    status = Column(Enum(FileStatus), default=FileStatus.UPLOADING)

    workspace = relationship("Workspace", back_populates="files")
    uploader = relationship("User")
    knowledge_bases = relationship("KnowledgeBase", secondary=knowledge_file_link, back_populates="files")

class KnowledgeBase(Base):
    __tablename__ = "knowledge_bases"
    
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    chunk_size = Column(Integer, default=1000)
    chunk_overlap = Column(Integer, default=200)

    workspace = relationship("Workspace", back_populates="knowledge_bases")
    files = relationship("File", secondary=knowledge_file_link, back_populates="knowledge_bases")