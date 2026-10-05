from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.domain.entities import BookingStatus


class CreateBookingRequest(BaseModel):
    showtime_id: int = Field(ge=1)
    seat_id: int = Field(ge=1)


class BookingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    showtime_id: int
    seat_id: int
    status: BookingStatus
    created_at: datetime


class BookingDetailsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    movie_title: str
    showtime_id: int
    start_time: datetime
    room_name: str
    seat_number: str
    status: BookingStatus
    created_at: datetime
    cancelled_at: datetime | None


class BookingListResponse(BaseModel):
    items: list[BookingDetailsResponse]
