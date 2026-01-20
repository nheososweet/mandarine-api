# app/db/base.py

# Import Base
from app.models.base_class import Base

# Import tất cả các model vào đây
# (Không cần dùng biến, chỉ cần import để nó được đăng ký vào Base.metadata)
from app.models.user import User
from app.models.workspace import Workspace, WorkspaceMember
from app.models.knowledge import File, KnowledgeBase
from app.models.agent import Agent, Tool
from app.models.chat import ChatSession, ChatMessage