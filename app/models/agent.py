from sqlalchemy import Column, String, Text, Boolean, ForeignKey, Enum, Table
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.models.base_class import Base
import enum

class AgentType(str, enum.Enum):
    BASIC = "BASIC"
    ORCHESTRATOR = "ORCHESTRATOR"

# N-N: Agent <-> Tool
agent_tool_link = Table(
    "agent_tool_links",
    Base.metadata,
    Column("agent_id", UUID(as_uuid=True), ForeignKey("agents.id", ondelete="CASCADE"), primary_key=True),
    Column("tool_id", UUID(as_uuid=True), ForeignKey("tools.id", ondelete="CASCADE"), primary_key=True)
)

# N-N: Agent <-> Knowledge
agent_knowledge_link = Table(
    "agent_knowledge_links",
    Base.metadata,
    Column("agent_id", UUID(as_uuid=True), ForeignKey("agents.id", ondelete="CASCADE"), primary_key=True),
    Column("knowledge_id", UUID(as_uuid=True), ForeignKey("knowledge_bases.id", ondelete="CASCADE"), primary_key=True)
)

class Tool(Base):
    name = Column(String, unique=True)
    func_name = Column(String, unique=True) 
    schema = Column(JSONB) 

class Agent(Base):
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False)
    
    name = Column(String, nullable=False)
    description = Column(Text)
    type = Column(Enum(AgentType), default=AgentType.BASIC)
    llm_model = Column(String, default="gpt-4o")
    system_instruction = Column(Text)
    
    # Config React Flow
    graph_config = Column(JSONB, nullable=True)
    is_public = Column(Boolean, default=False)

    workspace = relationship("Workspace", back_populates="agents")
    tools = relationship("Tool", secondary=agent_tool_link)
    knowledge_bases = relationship("KnowledgeBase", secondary=agent_knowledge_link)
    chat_sessions = relationship("ChatSession", back_populates="agent", cascade="all, delete-orphan")