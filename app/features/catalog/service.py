from app.domain.entities import Movie, Showtime, ShowtimeSeats
from app.domain.errors import FeatureNotReadyError
from app.features.catalog.contracts import CatalogRepository


class CatalogService:
    """Business layer. This module must never import FastAPI or SQLAlchemy."""

    def __init__(self, repository: CatalogRepository) -> None:
        self.repository = repository

    def list_movies(self) -> list[Movie]:
        raise FeatureNotReadyError(
            code="CATALOG_FEATURE_NOT_READY",
            message="Thành viên phụ trách catalog cần triển khai list_movies",
        )

    def list_showtimes(self, movie_id: int | None) -> list[Showtime]:
        raise FeatureNotReadyError(
            code="CATALOG_FEATURE_NOT_READY",
            message="Thành viên phụ trách catalog cần triển khai list_showtimes",
        )

    def list_seats(self, showtime_id: int) -> ShowtimeSeats:
        raise FeatureNotReadyError(
            code="CATALOG_FEATURE_NOT_READY",
            message="Thành viên phụ trách catalog cần triển khai list_seats",
        )
