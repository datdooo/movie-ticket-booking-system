from datetime import UTC, datetime, timedelta, timezone

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.models import BookingModel, MovieModel, RoomModel, SeatModel, ShowtimeModel, UserModel


@pytest.fixture
def booking_data(db_session: Session) -> tuple[int, int, int]:
    user = UserModel(email="db-test@example.com", password_hash="not-a-real-password")
    movie = MovieModel(title="Movie", duration_minutes=90)
    room = RoomModel(name="Room")
    db_session.add_all([user, movie, room])
    db_session.flush()
    seat = SeatModel(room_id=room.id, seat_number="A1")
    showtime = ShowtimeModel(
        movie_id=movie.id, room_id=room.id, start_time=datetime.now(UTC) + timedelta(days=1)
    )
    db_session.add_all([seat, showtime])
    db_session.commit()
    return user.id, showtime.id, seat.id


def test_database_prevents_duplicate_confirmed_seat(
    db_session: Session, booking_data: tuple[int, int, int]
) -> None:
    user_id, showtime_id, seat_id = booking_data
    db_session.add(BookingModel(user_id=user_id, showtime_id=showtime_id, seat_id=seat_id))
    db_session.commit()
    db_session.add(BookingModel(user_id=user_id, showtime_id=showtime_id, seat_id=seat_id))
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_cancelled_booking_releases_unique_seat(
    db_session: Session, booking_data: tuple[int, int, int]
) -> None:
    user_id, showtime_id, seat_id = booking_data
    db_session.add_all(
        [
            BookingModel(
                user_id=user_id,
                showtime_id=showtime_id,
                seat_id=seat_id,
                status="CANCELLED",
                cancelled_at=datetime.now(UTC),
            ),
            BookingModel(user_id=user_id, showtime_id=showtime_id, seat_id=seat_id),
        ]
    )
    db_session.commit()
    assert len(list(db_session.scalars(select(BookingModel)))) == 2


def test_foreign_keys_are_enabled(db_session: Session) -> None:
    db_session.add(SeatModel(room_id=99999, seat_number="A1"))
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_sqlite_round_trip_keeps_utc_timezone(
    db_session: Session, booking_data: tuple[int, int, int]
) -> None:
    _, showtime_id, _ = booking_data
    instant = datetime(2026, 10, 10, 19, 30, tzinfo=timezone(timedelta(hours=7)))
    showtime = db_session.get(ShowtimeModel, showtime_id)
    showtime.start_time = instant
    db_session.commit()
    db_session.expire_all()
    reloaded = db_session.get(ShowtimeModel, showtime_id)
    assert reloaded.start_time.tzinfo is UTC
    assert reloaded.start_time == datetime(2026, 10, 10, 12, 30, tzinfo=UTC)
