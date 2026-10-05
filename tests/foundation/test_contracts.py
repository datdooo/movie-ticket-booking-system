from datetime import UTC, datetime
from types import SimpleNamespace

from fastapi.testclient import TestClient

from app.core.config import get_settings
from app.core.security import create_access_token
from app.domain.entities import (
    BookingDetails,
    BookingStatus,
    SeatAvailability,
    SeatStatus,
    ShowtimeSeats,
)
from app.features.booking.dependencies import get_booking_service
from app.features.catalog.dependencies import get_catalog_service


def test_seat_response_contains_room_metadata(client: TestClient) -> None:
    seats = ShowtimeSeats(10, 1, "Phòng 1", [SeatAvailability(1, "A1", SeatStatus.AVAILABLE)])
    client.app.dependency_overrides[get_catalog_service] = lambda: SimpleNamespace(
        list_seats=lambda _: seats
    )
    response = client.get("/showtimes/10/seats")
    assert response.status_code == 200
    assert response.json() == {
        "showtime_id": 10,
        "room_id": 1,
        "room_name": "Phòng 1",
        "items": [{"id": 1, "seat_number": "A1", "status": "AVAILABLE"}],
    }


def test_booking_detail_passes_jwt_identity_and_hides_internal_owner(client: TestClient) -> None:
    now = datetime.now(UTC)
    detail = BookingDetails(
        100, 7, "Interstellar", 10, now, "Phòng 1", "A1", BookingStatus.CONFIRMED, now, None
    )
    calls = []

    def get_details(booking_id, user_id):
        calls.append((booking_id, user_id))
        return detail

    client.app.dependency_overrides[get_booking_service] = lambda: SimpleNamespace(
        get_booking_details=get_details
    )
    token = create_access_token(7, get_settings())
    response = client.get("/bookings/100", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert calls == [(100, 7)]
    assert "user_id" not in response.json()
    assert set(response.json()) == {
        "id",
        "movie_title",
        "showtime_id",
        "start_time",
        "room_name",
        "seat_number",
        "status",
        "created_at",
        "cancelled_at",
    }
