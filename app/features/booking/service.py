from app.domain.entities import Booking, BookingDetails
from app.domain.errors import FeatureNotReadyError
from app.features.booking.contracts import BookingRepository


class BookingService:
    """Business layer. This module must never import FastAPI or SQLAlchemy."""

    def __init__(self, repository: BookingRepository) -> None:
        self.repository = repository

    def create_booking(
        self,
        user_id: int,
        showtime_id: int,
        seat_id: int,
    ) -> Booking:
        raise FeatureNotReadyError(
            code="BOOKING_FEATURE_NOT_READY",
            message="Thành viên phụ trách booking cần triển khai create_booking",
        )

    def list_my_bookings(self, user_id: int) -> list[BookingDetails]:
        raise FeatureNotReadyError(
            code="BOOKING_FEATURE_NOT_READY",
            message="Thành viên phụ trách booking cần triển khai list_my_bookings",
        )

    def get_booking_details(self, booking_id: int, user_id: int) -> BookingDetails:
        raise FeatureNotReadyError(
            code="BOOKING_FEATURE_NOT_READY",
            message="Thành viên phụ trách booking cần triển khai get_booking_details",
        )

    def cancel_booking(self, booking_id: int, user_id: int) -> None:
        raise FeatureNotReadyError(
            code="BOOKING_FEATURE_NOT_READY",
            message="Thành viên phụ trách booking cần triển khai cancel_booking",
        )
