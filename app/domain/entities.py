from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class BookingStatus(StrEnum):
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"


class SeatStatus(StrEnum):
    AVAILABLE = "AVAILABLE"
    BOOKED = "BOOKED"


@dataclass(frozen=True, slots=True)
class User:
    id: int
    email: str
    password_hash: str
    created_at: datetime


@dataclass(frozen=True, slots=True)
class Movie:
    id: int
    title: str
    description: str | None
    duration_minutes: int
    poster_url: str | None


@dataclass(frozen=True, slots=True)
class Showtime:
    id: int
    movie_id: int
    movie_title: str
    room_id: int
    room_name: str
    start_time: datetime


@dataclass(frozen=True, slots=True)
class SeatAvailability:
    id: int
    seat_number: str
    status: SeatStatus


@dataclass(frozen=True, slots=True)
class Seat:
    id: int
    room_id: int
    seat_number: str


@dataclass(frozen=True, slots=True)
class ShowtimeSeats:
    showtime_id: int
    room_id: int
    room_name: str
    items: list[SeatAvailability]


@dataclass(frozen=True, slots=True)
class Booking:
    id: int
    user_id: int
    showtime_id: int
    seat_id: int
    status: BookingStatus
    created_at: datetime
    cancelled_at: datetime | None


@dataclass(frozen=True, slots=True)
class BookingDetails:
    id: int
    user_id: int
    movie_title: str
    showtime_id: int
    start_time: datetime
    room_name: str
    seat_number: str
    status: BookingStatus
    created_at: datetime
    cancelled_at: datetime | None
