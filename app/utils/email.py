from typing import List
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from app.core.config import settings
from pathlib import Path

# Cấu hình kết nối
conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=settings.USE_CREDENTIALS,
    VALIDATE_CERTS=settings.VALIDATE_CERTS
)

async def send_invite_email(email_to: str, workspace_name: str, invite_link: str):
    """
    Hàm gửi email mời thành viên
    """
    # Nội dung Email (HTML đơn giản)
    html = f"""
    <div style="font-family: Arial, sans-serif; padding: 20px;">
        <h2>🍊 Lời mời tham gia Workspace</h2>
        <p>Xin chào,</p>
        <p>Bạn đã được mời tham gia vào workspace <strong>{workspace_name}</strong> trên hệ thống Mandarine.</p>
        <p>Vui lòng click vào nút bên dưới để chấp nhận lời mời:</p>
        <a href="{invite_link}" style="background-color: #f97316; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">
            Tham gia ngay
        </a>
        <p style="margin-top: 20px; font-size: 12px; color: #666;">
            Link này sẽ hết hạn sau 24 giờ.<br>
            Nếu nút không hoạt động, hãy copy link này vào trình duyệt: {invite_link}
        </p>
    </div>
    """

    message = MessageSchema(
        subject=f"Mời tham gia Workspace: {workspace_name}",
        recipients=[email_to],
        body=html,
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    await fm.send_message(message)