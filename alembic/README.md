Generic single-database configuration.# Alembic Database Migrations

[English](#english) | [Tiếng Việt](#tiếng-việt)

---

## English

### Overview

This folder contains database migration files managed by Alembic, a lightweight database migration tool for SQLAlchemy. Alembic provides a way to manage database schema changes in a version-controlled manner.

### Folder Structure

```
alembic/
├── versions/          # Migration version files
├── env.py            # Alembic environment configuration
├── script.py.mako    # Template for generating new migrations
└── README.md         # This file
```

### Key Files

#### `env.py`

- Configures the Alembic migration environment
- Defines how migrations connect to your database
- Sets up SQLAlchemy engine and metadata
- Handles both offline and online migration modes

#### `script.py.mako`

- Template file used to generate new migration scripts
- Provides the standard structure for upgrade() and downgrade() functions
- Automatically used when running `alembic revision`

#### `versions/`

- Contains all migration version files
- Each file represents a specific database schema change
- Files are numbered sequentially and include revision IDs
- Never modify these files manually unless you know what you're doing

### Common Commands

#### Create a new migration

```bash
# Auto-generate migration by detecting model changes
alembic revision --autogenerate -m "description of changes"

# Create empty migration template
alembic revision -m "description of changes"
```

#### Apply migrations

```bash
# Upgrade to latest version
alembic upgrade head

# Upgrade to specific revision
alembic upgrade <revision_id>

# Upgrade by relative steps
alembic upgrade +2
```

#### Rollback migrations

```bash
# Downgrade by one revision
alembic downgrade -1

# Downgrade to specific revision
alembic downgrade <revision_id>

# Downgrade to base (remove all migrations)
alembic downgrade base
```

#### Check migration status

```bash
# Show current revision
alembic current

# Show migration history
alembic history

# Show pending migrations
alembic history -r current:head
```

### Best Practices

1. **Always review auto-generated migrations** before applying them
2. **Test migrations** in development environment first
3. **Backup your database** before running migrations in production
4. **Never modify existing migration files** that have been applied
5. **Use descriptive names** for migration messages
6. **Keep migrations small and focused** on specific changes
7. **Include both upgrade and downgrade** logic when possible

### Migration Workflow

1. Make changes to your SQLAlchemy models
2. Generate migration: `alembic revision --autogenerate -m "add user table"`
3. Review the generated migration file in `versions/`
4. Test the migration: `alembic upgrade head`
5. If needed, test rollback: `alembic downgrade -1`
6. Commit both model changes and migration file to version control

### Troubleshooting

#### Migration conflicts

If you get revision conflicts, check:

- Multiple developers created migrations simultaneously
- Migration history is out of sync
- Solution: Merge migrations or use `alembic merge` command

#### Database connection errors

- Verify database credentials in `alembic.ini` or environment variables
- Check network connectivity to database server
- Ensure database exists and user has proper permissions

#### Auto-generate not detecting changes

- Ensure models are properly imported in `env.py`
- Check that metadata is correctly set up
- Verify SQLAlchemy models are using declarative base

---

## Tiếng Việt

### Tổng quan

Thư mục này chứa các file migration (di chuyển) cơ sở dữ liệu được quản lý bởi Alembic, một công cụ migration nhẹ cho SQLAlchemy. Alembic cung cấp cách thức quản lý các thay đổi schema cơ sở dữ liệu theo phiên bản được kiểm soát.

### Cấu trúc thư mục

```
alembic/
├── versions/          # Các file phiên bản migration
├── env.py            # Cấu hình môi trường Alembic
├── script.py.mako    # Template để tạo migration mới
└── README.md         # File này
```

### Các file quan trọng

#### `env.py`

- Cấu hình môi trường migration của Alembic
- Định nghĩa cách migration kết nối với cơ sở dữ liệu
- Thiết lập SQLAlchemy engine và metadata
- Xử lý cả chế độ migration offline và online

#### `script.py.mako`

- File template được dùng để tạo script migration mới
- Cung cấp cấu trúc chuẩn cho các hàm upgrade() và downgrade()
- Tự động được sử dụng khi chạy lệnh `alembic revision`

#### `versions/`

- Chứa tất cả các file phiên bản migration
- Mỗi file đại diện cho một thay đổi schema cơ sở dữ liệu cụ thể
- Các file được đánh số tuần tự và bao gồm revision ID
- Không bao giờ sửa các file này thủ công trừ khi bạn biết rõ mình đang làm gì

### Các lệnh thường dùng

#### Tạo migration mới

```bash
# Tự động tạo migration bằng cách phát hiện thay đổi model
alembic revision --autogenerate -m "mô tả thay đổi"

# Tạo template migration trống
alembic revision -m "mô tả thay đổi"
```

#### Áp dụng migration

```bash
# Nâng cấp lên phiên bản mới nhất
alembic upgrade head

# Nâng cấp đến revision cụ thể
alembic upgrade <revision_id>

# Nâng cấp theo số bước tương đối
alembic upgrade +2
```

#### Quay lại migration cũ

```bash
# Hạ cấp xuống một revision
alembic downgrade -1

# Hạ cấp đến revision cụ thể
alembic downgrade <revision_id>

# Hạ cấp về base (xóa tất cả migration)
alembic downgrade base
```

#### Kiểm tra trạng thái migration

```bash
# Hiển thị revision hiện tại
alembic current

# Hiển thị lịch sử migration
alembic history

# Hiển thị các migration chưa áp dụng
alembic history -r current:head
```

### Các thực hành tốt nhất

1. **Luôn xem xét migration tự động tạo** trước khi áp dụng
2. **Kiểm thử migration** trong môi trường phát triển trước
3. **Sao lưu cơ sở dữ liệu** trước khi chạy migration trong production
4. **Không bao giờ sửa đổi các file migration đã áp dụng**
5. **Sử dụng tên mô tả rõ ràng** cho thông điệp migration
6. **Giữ migration nhỏ và tập trung** vào các thay đổi cụ thể
7. **Bao gồm cả logic upgrade và downgrade** khi có thể

### Quy trình làm việc với Migration

1. Thực hiện thay đổi trên các model SQLAlchemy
2. Tạo migration: `alembic revision --autogenerate -m "thêm bảng user"`
3. Xem xét file migration được tạo trong `versions/`
4. Kiểm thử migration: `alembic upgrade head`
5. Nếu cần, kiểm thử rollback: `alembic downgrade -1`
6. Commit cả thay đổi model và file migration vào version control

### Xử lý sự cố

#### Xung đột migration

Nếu gặp xung đột revision, kiểm tra:

- Nhiều developer tạo migration cùng lúc
- Lịch sử migration không đồng bộ
- Giải pháp: Gộp migration hoặc dùng lệnh `alembic merge`

#### Lỗi kết nối cơ sở dữ liệu

- Xác minh thông tin đăng nhập database trong `alembic.ini` hoặc biến môi trường
- Kiểm tra kết nối mạng đến database server
- Đảm bảo database tồn tại và user có quyền phù hợp

#### Auto-generate không phát hiện thay đổi

- Đảm bảo các model được import đúng trong `env.py`
- Kiểm tra metadata được thiết lập chính xác
- Xác minh các model SQLAlchemy đang sử dụng declarative base

---

## Additional Resources / Tài liệu tham khảo

- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Migration Best Practices](https://alembic.sqlalchemy.org/en/latest/tutorial.html)

---

**Note / Lưu ý**: Always coordinate with your team when creating and applying migrations to avoid conflicts / Luôn phối hợp với team khi tạo và áp dụng migration để tránh xung đột.
