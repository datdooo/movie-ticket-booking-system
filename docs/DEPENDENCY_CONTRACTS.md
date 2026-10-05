# Hợp đồng Service và Repository

Các chữ ký trong `contracts.py` đã được chốt trước khi tách ba nhánh. Service chỉ
nhận entity Python từ Repository. `dependencies.py` của mỗi feature nối Session,
Repository và Service; router không tự khởi tạo ORM adapter.

## Auth

- `UserRepository.get_by_email(email) -> User | None`: truy vấn email đã chuẩn hóa.
- `UserRepository.add(email, password_hash) -> User`: insert và commit; chuyển
  unique email thành `ConflictError("EMAIL_ALREADY_EXISTS", ...)`.
- `AuthService.register(email, password) -> User`: trim/lowercase, hash, gọi add.
- `AuthService.login(email, password) -> str`: kiểm tra hash; dùng
  `create_access_token(user.id, get_settings())` từ `app/core/security.py`.
- JWT phải có `sub`, `iat`, `exp`. Middleware decode một lần; dependency booking
  chỉ áp policy và lấy user id đã decode. Không viết lại JWT trong endpoint.

## Catalog

- `list_active_movies() -> list[Movie]`: chỉ active, id tăng dần.
- `list_showtimes(movie_id) -> list[Showtime]`: start_time tăng dần.
- `get_showtime(showtime_id) -> Showtime | None`: lấy thông tin phòng và suất.
- `list_seat_availability(showtime_id) -> list[SeatAvailability]`: ghế của phòng
  suất chiếu, BOOKED chỉ khi có booking CONFIRMED.
- `CatalogService.list_seats(showtime_id) -> ShowtimeSeats`: quyết định 404 nếu
  suất không tồn tại và ghép `showtime_id`, `room_id`, `room_name`, `items`.

## Booking

| Repository method | Kết quả | Mục đích của Service |
| --- | --- | --- |
| `get_showtime(showtime_id)` | `Showtime | None` | Kiểm tra tồn tại, giờ bắt đầu và phòng |
| `get_seat(seat_id)` | `Seat | None` | Kiểm tra tồn tại và seat.room_id |
| `has_confirmed_booking(showtime_id, seat_id)` | `bool` | Báo ghế đã được đặt trước insert |
| `create(user_id, showtime_id, seat_id)` | `Booking` | Insert/commit trong transaction |
| `list_by_user(user_id)` | `list[BookingDetails]` | Danh sách vé riêng user, mới nhất trước |
| `get_by_id(booking_id)` | `Booking | None` | Kiểm tra owner/status trước hủy |
| `get_details(booking_id)` | `BookingDetails | None` | Kiểm tra owner và trả chi tiết |
| `cancel(booking_id, cancelled_at)` | `None` | Ghi CANCELLED + cancelled_at và commit |

`BookingDetails.user_id` là field nội bộ để Service kiểm tra quyền; không xuất
hiện trong response xem vé. Service quyết định 404, 403, 400 hoặc 409 qua các
exception trong `app/domain/errors.py`.

Repository không kiểm tra quyền user. `cancel()` không nhận user_id; Service phải
gọi `get_by_id()` và kiểm tra owner/status trước đó. Repository cũng phải bảo đảm
transaction khi cập nhật. Không dùng GET để thay đổi dữ liệu.

Sau kiểm tra sớm, hai request vẫn có thể tranh cùng ghế. Partial unique index là
ràng buộc cuối; `create()` phải rollback và chuyển IntegrityError của index này
thành `ConflictError("SEAT_ALREADY_BOOKED", ...)`. Không chuyển mọi IntegrityError
thành lỗi ghế trùng vì lỗi FK hoặc constraint khác có nguyên nhân khác.

## Datetime và test

- Dùng `datetime.now(UTC)`; không dùng datetime.now() không timezone.
- `UTCDateTime` trong tầng DB giữ UTC khi SQLite trả lại datetime không timezone.
- Unit Service dùng fake repository; không dùng FastAPI hoặc SQLAlchemy.
- Test Repository dùng fixture `db_session`. Test đồng thời dùng
  `db_session_factory`, mỗi luồng/session riêng.
- Client API dùng một Session riêng cho mỗi request; lifespan test không tạo DB
  demo. Dữ liệu được seed trong session test cần commit trước khi gọi API.
- Test T22/T23 (details chính chủ/người khác) và các business tests còn lại do
  người sở hữu feature viết khi thay stub. Test foundation không chứng minh
  nghiệp vụ đã triển khai.
