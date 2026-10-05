# Phân công ba feature không chồng file

## Ownership

| Thành viên | Feature | Được sửa chính | Test bắt buộc |
| --- | --- | --- | --- |
| Chiến | Auth | `app/features/auth/**`, `tests/auth/**` | register, login, normalize email, hash password, JWT |
| Hải | Catalog | `app/features/catalog/**`, `tests/catalog/**` | movies, showtimes, filter, seats availability |
| Đạt | Booking | `app/features/booking/**`, `tests/booking/**` | create/list/details/cancel, ownership, transaction, concurrency |

## File chung đã khóa ở baseline

Không sửa trực tiếp các file sau trong ba feature PR:

- `app/main.py`
- `app/api/**`, `app/core/**`, `app/db/**`, `app/domain/**`
- `tests/conftest.py`
- `tests/foundation/**`, `tests/architecture/**`, `tests/smoke/**`
- `.github/**`, Docker/config/dependencies và `scripts/**`

Nếu phát hiện contract thiếu, người phát hiện mở issue. Một người được chỉ định tạo
PR `chore/foundation-<mô-tả>`; merge PR này trước, sau đó cả ba nhánh cập nhật lại.

CI kiểm tra ba nhánh feature bằng `scripts/check_feature_scope.py`: một PR
`feature/auth` chỉ được đổi `app/features/auth/**` và `tests/auth/**`; hai feature
còn lại tương tự. PR foundation/integration cần cả nhóm review vì có thể đổi file
chung. Quy tắc này giảm conflict; không bảo đảm mọi lần merge đều không conflict.

Mỗi feature có `dependencies.py` riêng nên không cần cùng sửa `main.py` hoặc
router chung. Chi tiết chữ ký đã khóa ở `docs/DEPENDENCY_CONTRACTS.md`.

## Definition of Done theo feature

### Auth

- Email trim và lowercase trước lookup.
- Password chỉ lưu hash.
- Email trùng trả `409 EMAIL_ALREADY_EXISTS`.
- Login sai trả `401 INVALID_CREDENTIALS`.
- JWT `sub` là chuỗi của user id và có expiry.
- Không sửa middleware; dùng helper trong `app/core/security.py`.

### Catalog

- Chỉ trả movie `is_active=true`, sắp xếp `id` tăng dần.
- Showtime lọc được theo `movie_id`, sắp xếp `start_time` tăng dần.
- Showtime không tồn tại trả `404 SHOWTIME_NOT_FOUND`.
- Ghế BOOKED chỉ khi có booking CONFIRMED cùng showtime và seat.
- Booking CANCELLED không giữ ghế.

### Booking

- Kiểm tra showtime, seat, thời gian và room trước insert.
- Tạo booking trong transaction.
- Repository chuyển `IntegrityError` của partial unique index thành
  `ConflictError`; API ánh xạ thành `409 SEAT_ALREADY_BOOKED`.
- `GET /bookings/me` luôn lọc theo user id từ JWT.
- `GET /bookings/{booking_id}` chỉ trả vé thuộc current user.
- DELETE là soft delete và giải phóng ghế.
- Concurrency test chứng minh một `201` và một `409`.

## Phần chung cuối pha

- Chiến: phối hợp test tích hợp đăng ký → login → đặt → list → details → hủy.
- Hải: dữ liệu demo, chạy Docker build/health/seed và hỗ trợ kiểm thử Catalog.
- Đạt: concurrency test và ba mức tải Kaggle CPU; báo cáo commit SHA, RPS,
  median/p95/p99 và error rate. Gửi kết quả trong PR tải riêng.
- Cả nhóm: bảo vệ `main`, review PR và chạy CI trước merge. Không thêm collaborator
  bằng tên hiển thị; cần GitHub username thực của mỗi người.

## Thứ tự merge

1. `feature/auth`
2. `feature/catalog`
3. `feature/booking`
4. `test/integration-flow`
5. `docs/final-demo`

Mỗi PR merge xong phải chạy lại toàn bộ CI. Không chờ cả ba feature xong mới merge.
