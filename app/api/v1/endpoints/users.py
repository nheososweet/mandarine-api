from fastapi import APIRouter, Depends
from app.api import deps
from app.schemas.user import UserResponse
from app.models.user import User

router = APIRouter()

# 👇 Swagger chỉ hiện ổ khóa nếu dòng này tồn tại và được load thành công
@router.get("/me", response_model=UserResponse)
def read_user_me(
    current_user: User = Depends(deps.get_current_user),
):
    return current_user