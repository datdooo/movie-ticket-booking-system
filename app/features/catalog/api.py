from typing import Annotated

from fastapi import APIRouter, Path, Query

from app.features.catalog.dependencies import CatalogServiceDependency
from app.features.catalog.schemas import (
    MovieListResponse,
    MovieResponse,
    SeatListResponse,
    ShowtimeListResponse,
    ShowtimeResponse,
)

router = APIRouter(tags=["catalog"])


@router.get("/movies", response_model=MovieListResponse, operation_id="list_movies")
def list_movies(service: CatalogServiceDependency) -> MovieListResponse:
    movies = service.list_movies()
    return MovieListResponse(items=[MovieResponse.model_validate(item) for item in movies])


@router.get(
    "/showtimes",
    response_model=ShowtimeListResponse,
    operation_id="list_showtimes",
)
def list_showtimes(
    service: CatalogServiceDependency,
    movie_id: Annotated[int | None, Query(ge=1)] = None,
) -> ShowtimeListResponse:
    showtimes = service.list_showtimes(movie_id)
    return ShowtimeListResponse(items=[ShowtimeResponse.model_validate(item) for item in showtimes])


@router.get(
    "/showtimes/{showtime_id}/seats",
    response_model=SeatListResponse,
    operation_id="list_showtime_seats",
)
def list_showtime_seats(
    service: CatalogServiceDependency,
    showtime_id: Annotated[int, Path(ge=1)],
) -> SeatListResponse:
    seats = service.list_seats(showtime_id)
    return SeatListResponse.model_validate(seats)
