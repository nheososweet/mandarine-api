from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, workspaces

api_router = APIRouter()

# Đăng ký router Auth vào hệ thống
# Các API sẽ có prefix là /auth (VD: /api/v1/auth/login)
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(workspaces.router, prefix="/workspaces", tags=["workspaces"])