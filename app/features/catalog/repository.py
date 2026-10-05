from sqlalchemy.orm import Session

from app.domain.entities import Movie, SeatAvailability, Showtime
from app.domain.errors import FeatureNotReadyError


class SqlAlchemyCatalogRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list_active_movies(self) -> list[Movie]:
        raise FeatureNotReadyError(
            code="CATALOG_REPOSITORY_NOT_READY",
            message="Triển khai truy vấn phim active trong feature/catalog/repository.py",
        )

    def list_showtimes(self, movie_id: int | None) -> list[Showtime]:
        raise FeatureNotReadyError(
            code="CATALOG_REPOSITORY_NOT_READY",
            message="Triển khai truy vấn suất chiếu trong feature/catalog/repository.py",
        )

    def get_showtime(self, showtime_id: int) -> Showtime | None:
        raise FeatureNotReadyError(
            code="CATALOG_REPOSITORY_NOT_READY",
            message="Triển khai truy vấn suất chiếu trong feature/catalog/repository.py",
        )

    def list_seat_availability(self, showtime_id: int) -> list[SeatAvailability]:
        raise FeatureNotReadyError(
            code="CATALOG_REPOSITORY_NOT_READY",
            message="Triển khai trạng thái ghế trong feature/catalog/repository.py",
        )
