# Kiểm tra lại skeleton theo đặc tả v1.2

Ngày kiểm tra: 05/10/2026. Phạm vi: khung dùng chung trước khi chia ba feature.

## Kết luận

Khung đã có đủ route, schema, entity, repository ports, DI, ORM constraints,
middleware, cấu hình, seed, CI và tài liệu để ba người bắt đầu triển khai.
Các chức năng Auth/Catalog/Booking vẫn là stub và trả 501. Đây chưa phải backend
đã hoàn thành Pha 1. Test nền pass không thay thế business tests hoặc demo đầy đủ.

## Thiếu sót tìm được và đã sửa

| Điểm cũ | Sửa trong baseline đã review |
| --- | --- |
| Booking ports không có dữ liệu để Service kiểm tra showtime, seat, owner/status | Thêm get_showtime, get_seat, get_by_id và has_confirmed_booking |
| cancel nhận user_id, dễ đẩy quyền nghiệp vụ xuống Repository | Service lấy booking/kiểm tra quyền; Repository nhận id và cancelled_at |
| Response seats thiếu room_id/room_name của đặc tả | Entity ShowtimeSeats và schema đủ metadata phòng |
| Router import ORM/adapter trực tiếp, lệch quy tắc phụ thuộc | dependencies.py riêng của mỗi feature nối Service và Repository |
| JWT không có expiry vẫn được chấp nhận | Bắt buộc sub/iat/exp và test token không exp/hết hạn/sai chữ ký |
| .env.example có nhưng .env không được đọc | load_dotenv; biến đã export được ưu tiên |
| SQLite đọc datetime không timezone | UTCDateTime chuẩn hóa UTC và test round trip |
| Lifespan test khởi tạo DB demo; client dùng chung Session | Tắt init DB trong app test; Session riêng từng request, factory cho concurrency |
| AST test chỉ bắt import thư viện trực tiếp | Kiểm tra phụ thuộc gián tiếp, router boundary và cross-feature imports |
| Docker thiếu script seed và .dockerignore | Copy scripts; seed bằng compose exec; loại .env, DB và caches |
| Load chỉ gọi GET catalog và trộn /health vào thống kê | Full profile có auth, seats và booking lifecycle/details; health chỉ readiness |
| Load có thể đi tiếp khi API chưa healthy hoặc ghi đè các mức tải | Fail readiness; HTML/CSV/metadata riêng theo users; từ chối kết quả 0 request |
| Ownership mới nằm trong tài liệu | CI check_feature_scope cho ba nhánh feature |
| Lỗi HTTP/500 không dùng chung envelope | JSON error envelope và ErrorResponse trong Swagger |

## Kiểm chứng đã chạy

- Ruff format/check: pass.
- Pytest: 44 tests pass, gồm boundary, JWT, response contracts, SQL constraints,
  UTC, .env, seed chạy hai lần và scope checker trên Git diff thực.
- OpenAPI: đúng 9 method/path nghiệp vụ + GET /health; bốn thao tác booking có
  Bearer security. GET /bookings/me được khai báo trước route booking_id.
- Bash syntax, YAML CI/Compose và Locust user discovery: pass.
- Local load runner smoke: một user, nhận 501 từ stub register và trả exit 1;
  HTML/CSV có request lỗi đúng mong đợi. Chỉ trong công cụ QA cục bộ, tắt monitor
  CPU của Locust vì môi trường sandbox không đọc được process qua /proc. Code
  của repo giữ monitor mặc định. Kết quả này không phải benchmark Kaggle.
- Docker build/run chưa chạy local vì môi trường không có Docker. CI có job
  build image, kiểm tra health và seed hai lần để kiểm chứng trên GitHub runner.
- Có một deprecation warning từ Starlette TestClient/httpx của các dependencies
  cài trong môi trường; không có test failure.

## Các phần còn phải hoàn thành

1. Chiến triển khai AuthService/UserRepository và tests/auth.
2. Hải triển khai CatalogService/CatalogRepository và tests/catalog.
3. Đạt triển khai BookingService/BookingRepository và tests/booking, gồm T22/T23
   ownership của booking details và hai request cạnh tranh cùng ghế.
4. Cả nhóm chạy test tích hợp toàn luồng, CI Docker và demo trên DB mới.
5. Chạy ba mức tải thật trên Kaggle CPU và lưu báo cáo gắn commit SHA.
6. Owner bật bảo vệ main và thêm hai collaborator bằng GitHub username chính xác.

## Quy tắc tránh chồng file

Mỗi feature sở hữu app/features/<feature> và tests/<feature>. File foundation đã
khóa; sửa trong PR riêng và merge trước khi các nhánh cập nhật lại. CI phát hiện
sửa ngoài scope của ba nhánh chuẩn. Quy trình này giảm conflict, không bảo đảm
merge luôn không có conflict hoặc thay thế review của cả nhóm.

`app/db/models.py` là vị trí ORM thật; repo không có app/models/ riêng.
