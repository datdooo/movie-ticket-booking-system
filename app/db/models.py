from datetime import UTC, datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    ForeignKey,
    Index,
    String,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.types import UTCDateTime


def utc_now() -> datetime:
    return datetime.now(UTC)


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(UTCDateTime(), default=utc_now, nullable=False)


class MovieModel(Base):
    __tablename__ = "movies"
    __table_args__ = (CheckConstraint("duration_minutes > 0", name="ck_movies_duration"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    duration_minutes: Mapped[int] = mapped_column(nullable=False)
    poster_url: Mapped[str | None] = mapped_column(String(500))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(UTCDateTime(), default=utc_now, nullable=False)


class RoomModel(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(UTCDateTime(), default=utc_now, nullable=False)


class SeatModel(Base):
    __tablename__ = "seats"
    __table_args__ = (UniqueConstraint("room_id", "seat_number", name="uq_room_seat"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    room_id: Mapped[int] = mapped_column(
        ForeignKey("rooms.id", ondelete="RESTRICT"), nullable=False
    )
    seat_number: Mapped[str] = mapped_column(String(10), nullable=False)


class ShowtimeModel(Base):
    __tablename__ = "showtimes"
    __table_args__ = (
        UniqueConstraint("room_id", "start_time", name="uq_room_start"),
        Index("idx_showtimes_movie_time", "movie_id", "start_time"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    movie_id: Mapped[int] = mapped_column(
        ForeignKey("movies.id", ondelete="RESTRICT"), nullable=False
    )
    room_id: Mapped[int] = mapped_column(
        ForeignKey("rooms.id", ondelete="RESTRICT"), nullable=False
    )
    start_time: Mapped[datetime] = mapped_column(UTCDateTime(), nullable=False)
    created_at: Mapped[datetime] = mapped_column(UTCDateTime(), default=utc_now, nullable=False)


class BookingModel(Base):
    __tablename__ = "bookings"
    __table_args__ = (
        CheckConstraint("status IN ('CONFIRMED', 'CANCELLED')", name="ck_bookings_status"),
        CheckConstraint(
            "(status = 'CONFIRMED' AND cancelled_at IS NULL) OR "
            "(status = 'CANCELLED' AND cancelled_at IS NOT NULL)",
            name="ck_bookings_cancelled_at",
        ),
        Index("idx_bookings_user", "user_id"),
        Index("idx_bookings_showtime", "showtime_id"),
        Index(
            "uq_confirmed_booking_seat",
            "showtime_id",
            "seat_id",
            unique=True,
            sqlite_where=text("status = 'CONFIRMED'"),
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    showtime_id: Mapped[int] = mapped_column(
        ForeignKey("showtimes.id", ondelete="RESTRICT"), nullable=False
    )
    seat_id: Mapped[int] = mapped_column(
        ForeignKey("seats.id", ondelete="RESTRICT"), nullable=False
    )
    status: Mapped[str] = mapped_column(String(20), default="CONFIRMED", nullable=False)
    created_at: Mapped[datetime] = mapped_column(UTCDateTime(), default=utc_now, nullable=False)
    cancelled_at: Mapped[datetime | None] = mapped_column(UTCDateTime())
