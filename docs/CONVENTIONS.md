# Quy ước code và API đã khóa

Tài liệu này là contract chung. Không tự đổi tên field hoặc kiểu dữ liệu trong
feature riêng. Thay đổi contract phải đi bằng một PR nhỏ và được cả nhóm xác nhận.

## Tên trong Python

| Loại | Quy ước | Ví dụ |
| --- | --- | --- |
| File và module | `snake_case` | `repository.py`, `seat_status.py` |
| Hàm và biến | `snake_case` | `list_showtimes`, `current_user_id` |
| Class | `PascalCase` | `BookingService`, `CreateBookingRequest` |
| Hằng số | `UPPER_SNAKE_CASE` | `ACCESS_TOKEN_EXPIRE_MINUTES` |
| Boolean | tiền tố `is_`, `has_`, `can_` | `is_active` |
| Datetime | hậu tố `_at` hoặc `_time` | `created_at`, `start_time` |

Chỉ dùng absolute import bắt đầu bằng `app.`. Không dùng wildcard import.

## Tên database

- Tên bảng số nhiều, `snake_case`: `users`, `showtimes`, `bookings`.
- Khóa chính luôn là `id`.
- Khóa ngoại là `<entity>_id`: `movie_id`, `showtime_id`.
- Enum lưu chữ hoa: `CONFIRMED`, `CANCELLED`, `AVAILABLE`, `BOOKED`.
- Tất cả datetime được hiểu là UTC và trả về ISO 8601.
- Entity datetime luôn có timezone UTC; DB dùng `UTCDateTime` cho SQLite.
- Không đổi sáu ORM model trong feature PR. Nếu bắt buộc đổi, tạo PR database riêng.

## Tên schema

- Body vào: `<Action><Entity>Request`, ví dụ `CreateBookingRequest`.
- Object ra: `<Entity>Response`, ví dụ `BookingResponse`.
- Danh sách ra: `<Entity>ListResponse` và field duy nhất là `items`.
- Không trả `password` hoặc `password_hash`.

## Tên service và repository

- Service dùng động từ nghiệp vụ: `register`, `login`, `create_booking`,
  `cancel_booking`.
- Repository dùng động từ dữ liệu: `get_by_email`, `list_by_user`, `add`, `cancel`.
- Service không nhận `Request`, `Response`, `Session` hoặc SQLAlchemy model.
- Repository không quyết định HTTP status hay quyền nghiệp vụ.
- SQLAlchemy IntegrityError chỉ được bắt và rollback trong Repository, rồi đổi
  thành exception thuần Python. Service không import IntegrityError.
- Router lấy Service qua dependency riêng của feature; không import ORM trực tiếp.

## HTTP và lỗi

- Path dùng danh từ số nhiều: `/movies`, `/showtimes`, `/bookings`.
- Request/response dùng JSON, trừ `204 No Content`.
- Lỗi luôn có dạng:

```json
{
  "error": {
    "code": "SEAT_ALREADY_BOOKED",
    "message": "Ghế đã được đặt"
  }
}
```

- `401`: thiếu/sai/hết hạn token.
- `403`: đã xác thực nhưng không có quyền.
- `404`: resource không tồn tại.
- `409`: xung đột trạng thái hoặc unique constraint.
- `422`: input không đúng schema.

## Git

- Nhánh: `feature/auth`, `feature/catalog`, `feature/booking`.
- Commit: Conventional Commits như `feat(auth): ...`, `test(catalog): ...`.
- Không format toàn repo trong feature PR.
- Không sửa import/order ở file feature khác chỉ vì IDE tự động.
- Trước PR: merge/rebase `main`, chạy `ruff check .` và `pytest`.
