# Phân công ba feature không chồng file

## Ownership

| Thành viên | Feature | Được sửa chính | Test bắt buộc |
| --- | --- | --- | --- |
| Chiến | Auth | `app/features/auth/**`, `tests/auth/**` | register, login, normalize email, hash password, JWT |
| Hải | Catalog | `app/features/catalog/**`, `tests/catalog/**` | movies, showtimes, filter, seats availability |
| Đạt | Booking | `app/features/booking/**`, `tests/booking/**` | create/list/details/cancel, ownership, transaction, concurrency |

## Phần phụ đã phân công

Foundation đã có trong skeleton. Hải chịu trách nhiệm kiểm chứng, chuẩn bị dữ liệu
và xử lý lỗi nền được phát hiện; không cần dựng lại khung. Phần phụ là công việc
cần hoàn thành, không phải xác nhận rằng baseline đã chạy hết nghiệp vụ.

| Thành viên | Phần phụ sở hữu | Đầu ra cần bàn giao |
| --- | --- | --- |
| Hải | Kiểm chứng Foundation, Docker và dữ liệu demo; kiểm thử tải Kaggle CPU | Hướng dẫn chạy được trên môi trường mới; build/health/seed thành công; HTML, CSV và báo cáo tải ba mức 10/50/100 users |
| Chiến | Test tích hợp; đối chiếu Swagger/API contract; tài liệu và kịch bản demo | Test toàn luồng và quyền sở hữu; README chạy đúng; tài liệu khớp code và demo có thể chạy lại |
| Đạt | Transaction, rollback và concurrency của Booking | Test một 201 và một 409 khi tranh cùng ghế; hủy giải phóng ghế; đặt lại tạo booking mới |

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

- Hải: kiểm chứng ứng dụng trên môi trường mới; Docker build, health và seed;
  chuẩn bị dữ liệu demo có suất tương lai. Phụ trách kiểm thử tải toàn luồng trên
  Kaggle CPU ở ba mức 10/50/100 users; lưu HTML, CSV và báo cáo commit SHA,
  CPU/RAM, RPS, median, p95, p99 và error rate. Phân loại lỗi và chuyển cho người
  sở hữu feature xử lý. Script seed đã có; chỉ sửa khi kiểm chứng cho thấy cần.
- Chiến: phụ trách test tích hợp đăng ký → đăng nhập → tra cứu → đặt vé →
  danh sách → chi tiết → hủy → đặt lại. Kiểm tra quyền sở hữu bằng hai tài khoản,
  gồm xem chi tiết và hủy vé của người khác. Đối chiếu Swagger với API contract;
  hoàn thiện README, hướng dẫn chạy và kịch bản demo theo code đã tích hợp.
- Đạt: hoàn thiện Booking, transaction, rollback và concurrency test. Chứng minh
  hai request cùng ghế chỉ tạo một booking CONFIRMED; hủy giải phóng ghế và đặt
  lại tạo booking mới. Xử lý lỗi Booking được phát hiện trong test tích hợp
  hoặc kiểm thử tải.
- Cả nhóm: bảo vệ `main`, review PR và chạy CI trước merge. Không thêm collaborator
  bằng tên hiển thị; cần GitHub username thực của mỗi người. Chỉ chạy báo cáo tải
  cuối sau khi cả ba feature đã hoàn thành và test tích hợp đã pass.

Người chạy test không nhận thay ownership của feature lỗi: Hải sửa Catalog,
Chiến sửa Auth và Đạt sửa Booking. Lỗi nền dùng chung được xử lý trong PR riêng
bởi người đã được chỉ định.

## Nhánh và phạm vi PR phần phụ

Các nhánh dưới đây là nhánh công việc tạo từ `main` mới nhất khi bắt đầu; không
thay thế ba nhánh feature hoặc tạo thêm nhánh tích hợp thường trực.

| Phụ trách | Nhánh đề xuất | Phạm vi chính |
| --- | --- | --- |
| Hải | `chore/foundation-demo` | Kiểm chứng Docker/config/seed; sửa lỗi nền hoặc dữ liệu demo nếu cần |
| Chiến | `test/integration-flow` | `tests/integration/**` để test toàn luồng; fixture dùng chung chỉ đổi khi cần |
| Hải | `test/kaggle-load` | `tests/load/**`, `scripts/run_kaggle_load_test.sh` nếu cần sửa; báo cáo tại `docs/load-results/**` |
| Chiến | `docs/final-demo` | README, đối chiếu `docs/API_CONTRACT.md`, tài liệu bàn giao và `docs/DEMO.md` |

Không đưa thay đổi phần phụ vào PR `feature/auth`, `feature/catalog` hoặc
`feature/booking`: CI giới hạn các nhánh đó theo thư mục feature và test riêng.
Ownership phần phụ không mở quyền sửa tùy ý file chung. PR thay đổi
`app/main.py`, `app/api/**`, `app/core/**`, `app/db/**`, `app/domain/**`,
`tests/conftest.py`, config hoặc dependencies cần cả nhóm review và chốt người
thực hiện. Đổi contract phải thống nhất trước, rồi cập nhật tài liệu và code.

Hải sở hữu nội dung kỹ thuật `docs/KAGGLE_LOAD_TEST.md` và báo cáo tải. Chiến
sở hữu README và tài liệu demo. Khi tổng hợp bàn giao, Chiến dẫn link báo cáo
của Hải; phối hợp trước nếu cần sửa cùng một tài liệu.

## Điều kiện review trước khi merge vào main

Mọi thay đổi vào `main` phải qua pull request và có ít nhất **1 APPROVE từ
người khác tác giả PR**. Nhận xét COMMENT không thay thế APPROVE. Chỉ merge khi
CI đã pass và các góp ý cần xử lý đã được giải quyết. Nếu có thay đổi nội dung
sau review, người review phải kiểm tra và approve lại; không tự approve hoặc
bỏ qua luật để merge. PR đổi file chung vẫn cần cả nhóm thống nhất theo quy định
ở trên.

Owner cấu hình branch protection/ruleset áp dụng cho `main`: Require a pull
request before merging, Require approvals = 1 và Dismiss stale pull request
approvals when new commits are pushed. Áp dụng cho cả người có quyền bypass,
không cho push trực tiếp vào `main`. Kiểm tra rule đã active trên GitHub; nội
dung trong docs không tự bật cấu hình bảo vệ nhánh.

## Thứ tự merge

1. `feature/auth`
2. `feature/catalog`
3. `feature/booking`
4. `test/integration-flow`
5. `test/kaggle-load`
6. `docs/final-demo`

PR `chore/foundation-demo` được merge khi cần; nếu sửa nền mà feature phụ thuộc,
merge trước feature đó rồi cập nhật các nhánh. Có thể chuẩn bị môi trường tải
sớm, nhưng chỉ chạy và chốt báo cáo toàn luồng sau bước 4.

Mỗi PR merge xong phải chạy lại toàn bộ CI. Không chờ cả ba feature xong mới merge.
