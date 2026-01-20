from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.api.v1.api import api_router
from app.db.base import Base
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Cấu hình CORS (Cho phép Frontend gọi API)
# Tạm thời cho phép tất cả (*) để dễ dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Nhúng toàn bộ Router API vào App
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # In lỗi ra Terminal để bạn thấy
    print(f"❌ LOI HE THONG: {str(exc)}")
    
    # Trả về JSON cho Frontend/Postman thấy rõ lỗi gì
    return JSONResponse(
        status_code=500,
        content={
            "message": "Internal Server Error",
            "detail": str(exc) # 👈 Đây chính là dòng lỗi cụ thể (VD: KeyError: 'Workspace')
        },
    )

# API Test đơn giản để biết server sống hay chết
@app.get("/")
def root():
    return {"message": "Welcome to Mandarine API Ecosystem 🍊"}