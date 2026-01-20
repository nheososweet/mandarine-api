"""rename_workspace_members

Revision ID: e554321b2d1c
Revises: 175837f94a4f
Create Date: 2026-01-20 14:00:47.421207

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'e554321b2d1c'
down_revision: Union[str, Sequence[str], None] = '175837f94a4f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Trong file alembic/versions/xxxx_rename_workspace_members.py

def upgrade() -> None:
    # 1. Đổi tên Bảng (workspacemembers -> workspace_members)
    op.rename_table('workspacemembers', 'workspace_members')

    # 2. Đổi tên Enum (workspacerole -> workspace_role)
    # Dùng lệnh SQL trực tiếp vì Alembic không hỗ trợ rename Enum
    op.execute('ALTER TYPE workspacerole RENAME TO workspace_role')


def downgrade() -> None:
    # 1. Đổi tên Enum ngược lại
    op.execute('ALTER TYPE workspace_role RENAME TO workspacerole')

    # 2. Đổi tên Bảng ngược lại
    op.rename_table('workspace_members', 'workspacemembers')