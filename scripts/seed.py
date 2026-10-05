from datetime import UTC, datetime, timedelta

from sqlalchemy import select

from app.db.models import MovieModel, RoomModel, SeatModel, ShowtimeModel
from app.db.session import SessionLocal, init_db


def seed() -> None:
    init_db()
    with SessionLocal.begin() as session:
        movies = list(session.scalars(select(MovieModel).order_by(MovieModel.id)))
        if not movies:
            movies = [
                MovieModel(
                    title="Interstellar",
                    description="A science fiction film",
                    duration_minutes=169,
                    poster_url=None,
                    is_active=True,
                ),
                MovieModel(
                    title="Spirited Away",
                    description="An animated fantasy film",
                    duration_minutes=125,
                    poster_url=None,
                    is_active=True,
                ),
                MovieModel(
                    title="The Dark Knight",
                    description="A superhero crime film",
                    duration_minutes=152,
                    poster_url=None,
                    is_active=True,
                ),
                MovieModel(
                    title="Inactive Demo Movie",
                    description="Used to test is_active filtering",
                    duration_minutes=90,
                    poster_url=None,
                    is_active=False,
                ),
            ]
            session.add_all(movies)
            session.flush()

        rooms = list(session.scalars(select(RoomModel).order_by(RoomModel.id)))
        if not rooms:
            rooms = [RoomModel(name="Phòng 1"), RoomModel(name="Phòng 2")]
            session.add_all(rooms)
            session.flush()

        if session.scalar(select(SeatModel.id).limit(1)) is None:
            for room in rooms:
                session.add_all(
                    [
                        SeatModel(room_id=room.id, seat_number=f"{row}{number}")
                        for row in ("A", "B")
                        for number in range(1, 11)
                    ]
                )

        if session.scalar(select(ShowtimeModel.id).limit(1)) is None:
            active_movies = [movie for movie in movies if movie.is_active]
            base_time = datetime.now(UTC).replace(minute=0, second=0, microsecond=0)
            for index, movie in enumerate(active_movies):
                session.add_all(
                    [
                        ShowtimeModel(
                            movie_id=movie.id,
                            room_id=rooms[0].id,
                            start_time=base_time + timedelta(days=1 + index, hours=2),
                        ),
                        ShowtimeModel(
                            movie_id=movie.id,
                            room_id=rooms[1].id,
                            start_time=base_time + timedelta(days=1 + index, hours=5),
                        ),
                    ]
                )

    print("Seed completed")


if __name__ == "__main__":
    seed()
