# API contract theo đặc tả v1.2

## Quy ước chung

- JSON cho request và response; `DELETE` thành công trả `204` không body.
- Datetime theo ISO 8601 và UTC.
- JWT: `Authorization: Bearer <access_token>`.
- Danh sách dùng `{ "items": [] }`.
- Error dùng `{ "error": { "code": "...", "message": "..." } }`.

## Endpoint và schema

### POST /auth/register

Request: `email`, `password`. Thành công `201`: `id`, `email`, `created_at`.

### POST /auth/login

Request: `email`, `password`. Thành công `200`: `access_token`, `token_type`.

### GET /movies

Thành công `200`: `items[]` gồm `id`, `title`, `description`,
`duration_minutes`, `poster_url`.

### GET /showtimes

Query tùy chọn `movie_id`. Thành công `200`: `items[]` gồm `id`, `movie_id`,
`movie_title`, `room_id`, `room_name`, `start_time`.

### GET /showtimes/{showtime_id}/seats

Thành công `200`: `showtime_id`, `room_id`, `room_name`, `items[]` gồm
`id`, `seat_number`, `status`.

### POST /bookings

JWT bắt buộc. Request: `showtime_id`, `seat_id`. Thành công `201`: `id`,
`user_id`, `showtime_id`, `seat_id`, `status`, `created_at`.

### GET /bookings/me

JWT bắt buộc. Thành công `200`: `items[]` gồm thông tin phim, suất, phòng, ghế,
trạng thái, `created_at`, `cancelled_at`.

### GET /bookings/{booking_id}

JWT bắt buộc. Trả chi tiết một vé thuộc current user, gồm thông tin phim, suất
chiếu, phòng, ghế, trạng thái, `created_at` và `cancelled_at`. Không tìm thấy
trả `404 BOOKING_NOT_FOUND`; booking thuộc user khác trả
`403 BOOKING_FORBIDDEN`.

### DELETE /bookings/{booking_id}

JWT bắt buộc. Hủy mềm booking của current user. Thành công `204`.

Contract chi tiết và bảng lỗi gốc nằm trong đặc tả hệ thống của nhóm. File này chỉ
là bản khóa nhanh để reviewer nhìn diff trong pull request.

## Lỗi nghiệp vụ đã chốt

| Endpoint | HTTP | error.code |
| --- | --- | --- |
| Register | 409 | `EMAIL_ALREADY_EXISTS` |
| Login | 401 | `INVALID_CREDENTIALS` |
| Các endpoint booking | 401 | `UNAUTHORIZED` |
| Seats hoặc create booking | 404 | `SHOWTIME_NOT_FOUND` |
| Create booking | 404 | `SEAT_NOT_FOUND` |
| Create booking | 400 | `SEAT_NOT_IN_SHOWTIME_ROOM` |
| Create booking | 409 | `SHOWTIME_ALREADY_STARTED`, `SEAT_ALREADY_BOOKED` |
| Details hoặc cancel | 404 | `BOOKING_NOT_FOUND` |
| Details hoặc cancel | 403 | `BOOKING_FORBIDDEN` |
| Cancel | 409 | `BOOKING_ALREADY_CANCELLED` |
| Input sai schema | 422 | `VALIDATION_ERROR` |

Các lỗi `AppError` được ánh xạ sang HTTP trong `app/api/errors.py`. Service không
tạo HTTPException và không bắt SQLAlchemy IntegrityError. Repository rollback
và chuyển lỗi unique constraint liên quan thành `ConflictError` đúng code.
