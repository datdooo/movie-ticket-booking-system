# Đối chiếu đặc tả với yêu cầu Pha 1

## Kết luận

Đặc tả v1.2 đã bổ sung booking details, middleware JWT, Docker, Kaggle CPU và
ranh giới Service không phụ thuộc web/DB. Skeleton được đối chiếu lại theo v1.2;
chi tiết sửa lỗi baseline và phần chưa triển khai nằm trong `SKELETON_AUDIT.md`.

| Yêu cầu của thầy | Đặc tả hiện tại | Xử lý trong baseline |
| --- | --- | --- |
| REST API và JSON | Đạt | Chốt chín endpoint nghiệp vụ |
| Có POST, GET, DELETE | Đạt | OpenAPI có đủ ba method |
| OpenAPI/Swagger | Đạt | FastAPI cung cấp `/docs` và `/openapi.json` |
| API -> nghiệp vụ -> dữ liệu | Đạt về ý tưởng | Tách `api`, `service`, `contracts`, `repository` theo feature |
| Service không import web/DB | v1.2 đã chốt | Entity và Protocol; test kiểm tra cả phụ thuộc gián tiếp |
| Hỗ trợ đăng nhập | Đạt | Giữ `/auth/login` và JWT Bearer |
| Một GET và một POST cần JWT | Đạt | `GET /bookings/me` và `POST /bookings` đều protected |
| Xác thực bằng middleware/filter/interceptor | v1.2 đã chốt | `AuthenticationMiddleware`; router booking khai báo policy một lần |
| Docker | v1.2 đã bổ sung | `Dockerfile`, Compose, seed trong container, Docker CI |
| GitHub public, README, commit rõ | Đạt về quy trình | Thêm README, CI và PR template |
| Chỉ chức năng cơ bản | Đạt | Không thêm admin, payment hay frontend |
| Kiểm thử tải Kaggle CPU | v1.2 đã bổ sung | Locust full flow và hướng dẫn ba mức tải; chưa có kết quả Kaggle |

## Các quyết định đã áp dụng ở v1.2

1. Đổi câu “Service được phép import Repository, Model” thành: Service chỉ import
   entity thuần Python và repository Protocol; không import SQLAlchemy model.
2. Ghi rõ JWT được giải mã tập trung trong middleware. Dependency tại router chỉ
   áp policy và đọc `request.state.current_user_id`.
3. Bổ sung mục đóng gói Docker và lệnh `docker compose up --build`.
4. Bổ sung kịch bản Locust chạy trên Kaggle CPU và chỉ số phải báo cáo.
5. Đổi “đúng 8 endpoint” thành “9 endpoint nghiệp vụ”; `/health` là endpoint kỹ thuật.
6. Ba tuần phát triển; tổng duyệt được ghi thành giai đoạn riêng, không còn mục
   tuần 4 gây lệch tiêu đề.
7. Quy định claim JWT `sub` là chuỗi biểu diễn `user_id`, sau khi decode mới ép về `int`.

## Quyết định phạm vi admin

Không cần trang hoặc API admin ở Pha 1. Seed script tạo phim, phòng, ghế và suất
chiếu để demo. Việc không làm admin không ảnh hưởng yêu cầu đăng nhập: login tồn
tại để xác định người đặt, bảo vệ booking của từng người và ngăn một user xem/hủy
booking của user khác.
