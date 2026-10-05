from datetime import datetime

from sqlalchemy.orm import Session

from app.domain.entities import Booking, BookingDetails, Seat, Showtime
from app.domain.errors import FeatureNotReadyError


class SqlAlchemyBookingRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_showtime(self, showtime_id: int) -> Showtime | None:
        raise FeatureNotReadyError(
            code="BOOKING_REPOSITORY_NOT_READY", message="Triển khai truy vấn suất chiếu"
        )

    def get_seat(self, seat_id: int) -> Seat | None:
        raise FeatureNotReadyError(
            code="BOOKING_REPOSITORY_NOT_READY", message="Triển khai truy vấn ghế"
        )

    def get_by_id(self, booking_id: int) -> Booking | None:
        raise FeatureNotReadyError(
            code="BOOKING_REPOSITORY_NOT_READY", message="Triển khai truy vấn booking"
        )

    def has_confirmed_booking(self, showtime_id: int, seat_id: int) -> bool:
        raise FeatureNotReadyError(
            code="BOOKING_REPOSITORY_NOT_READY", message="Triển khai kiểm tra ghế đã được đặt"
        )

    def create(self, user_id: int, showtime_id: int, seat_id: int) -> Booking:
        raise FeatureNotReadyError(
            code="BOOKING_REPOSITORY_NOT_READY",
            message="Triển khai transaction đặt ghế trong feature/booking/repository.py",
        )

    def list_by_user(self, user_id: int) -> list[BookingDetails]:
        raise FeatureNotReadyError(
            code="BOOKING_REPOSITORY_NOT_READY",
            message="Triển khai danh sách booking trong feature/booking/repository.py",
        )

    def get_details(self, booking_id: int) -> BookingDetails | None:
        raise FeatureNotReadyError(
            code="BOOKING_REPOSITORY_NOT_READY",
            message="Triển khai chi tiết booking trong feature/booking/repository.py",
        )

    def cancel(self, booking_id: int, cancelled_at: datetime) -> None:
        raise FeatureNotReadyError(
            code="BOOKING_REPOSITORY_NOT_READY",
            message="Triển khai soft delete trong feature/booking/repository.py",
        )
