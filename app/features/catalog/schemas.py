from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.domain.entities import SeatStatus


class MovieResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    duration_minutes: int
    poster_url: str | None


class MovieListResponse(BaseModel):
    items: list[MovieResponse]


class ShowtimeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    movie_id: int
    movie_title: str
    room_id: int
    room_name: str
    start_time: datetime


class ShowtimeListResponse(BaseModel):
    items: list[ShowtimeResponse]


class SeatResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    seat_number: str
    status: SeatStatus


class SeatListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    showtime_id: int
    room_id: int
    room_name: str
    items: list[SeatResponse]
