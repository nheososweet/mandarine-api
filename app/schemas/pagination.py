from typing import Generic, TypeVar, List
from pydantic import BaseModel, Field

T = TypeVar("T")

# 1. Input: Dùng làm Dependency trong API
class PageParams(BaseModel):
    page: int = Field(1, ge=1, description="Page number (starts from 1)")
    size: int = Field(10, ge=1, le=100, description="Items per page")

# 2. Output: Cấu trúc JSON trả về chuẩn
class PagedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int
    pages: int