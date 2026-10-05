# Kiểm thử tải trên Kaggle CPU

## Mục tiêu

Chạy API và Locust trên cùng Kaggle Notebook dùng CPU, ghi lại throughput, latency
và error rate. Chỉ chạy sau khi ba feature đã hoàn thành; response `501` được tính
là lỗi và không được đưa vào báo cáo cuối.

## Cách chạy trong notebook

```bash
!git clone https://github.com/datdooo/movie-ticket-booking-system.git
%cd movie-ticket-booking-system
!pip install -q -r requirements-load.txt
!LOAD_USERS=50 LOAD_SPAWN_RATE=5 LOAD_RUN_TIME=60s bash scripts/run_kaggle_load_test.sh
```

Script tự seed, khởi động API và dừng ngay nếu API không healthy. Tải hoặc mở
`artifacts/locust-50u-report.html`. Chạy tối thiểu ba cấu hình:

| Lần | Users | Spawn rate | Thời gian |
| --- | ---: | ---: | ---: |
| 1 | 10 | 2/s | 60s |
| 2 | 50 | 5/s | 60s |
| 3 | 100 | 10/s | 60s |

```bash
!LOAD_USERS=10 LOAD_SPAWN_RATE=2 LOAD_RUN_TIME=60s bash scripts/run_kaggle_load_test.sh
!LOAD_USERS=50 LOAD_SPAWN_RATE=5 LOAD_RUN_TIME=60s bash scripts/run_kaggle_load_test.sh
!LOAD_USERS=100 LOAD_SPAWN_RATE=10 LOAD_RUN_TIME=60s bash scripts/run_kaggle_load_test.sh
```

Mỗi mức có HTML/CSV riêng và `*-metadata.json` chứa commit SHA, thời gian,
cấu hình tải và CPU. Ghi thêm RAM của Kaggle vào báo cáo. Dùng
`LOAD_REPORT_PREFIX` để giữ nhiều lần chạy cùng mức. Seed không reset bookings;
chuẩn bị database demo mới nếu dữ liệu cũ có showtime đã hết hạn.

Profile mặc định `LOAD_PROFILE=full`: mỗi user đăng ký/login một lần, sau đó gọi
movies/showtimes/seats, GET booking của mình, POST đặt vé, GET details và DELETE
hủy. Chọn ghế ngẫu nhiên trong danh sách AVAILABLE; 409 SEAT_ALREADY_BOOKED do
tranh ghế được tính là kết quả nghiệp vụ mong đợi và phải ghi rõ trong báo cáo.
401/500/501 hoặc status sai vẫn là lỗi và script trả exit code 1.

`LOAD_PROFILE=catalog` chỉ dùng kiểm tra Catalog riêng, không thay cho kết quả tải
toàn luồng. `/health` chỉ phục vụ readiness, không trộn vào thống kê nghiệp vụ.

## Chỉ số phải ghi vào báo cáo

- Tổng số request và request/second.
- Median, p95 và p99 response time.
- Số lượng và tỷ lệ request lỗi.
- Cấu hình Kaggle CPU/RAM tại thời điểm chạy.
- Commit SHA đã kiểm thử.

Tiêu chí tối thiểu cho demo: error rate bằng 0 đối với endpoint đã triển khai.
Không đặt ngưỡng latency cứng khi thầy chưa yêu cầu; báo trung thực kết quả của
từng mức tải và giải thích điểm bắt đầu suy giảm.
