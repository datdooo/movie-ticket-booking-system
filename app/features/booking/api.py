from typing import Annotated

from fastapi import APIRouter, Depends, Path, Response, status

from app.api.dependencies import current_user_id, require_authenticated_user
from app.features.booking.dependencies import BookingServiceDependency
from app.features.booking.schemas import (
    BookingDetailsResponse,
    BookingListResponse,
    BookingResponse,
    CreateBookingRequest,
)

router = APIRouter(
    prefix="/bookings",
    tags=["bookings"],
    dependencies=[Depends(require_authenticated_user)],
)
CurrentUserId = Annotated[int, Depends(current_user_id)]


@router.post(
    "",
    response_model=BookingResponse,
    status_code=status.HTTP_201_CREATED,
    operation_id="create_booking",
)
def create_booking(
    payload: CreateBookingRequest,
    service: BookingServiceDependency,
    user_id: CurrentUserId,
) -> BookingResponse:
    booking = service.create_booking(user_id, payload.showtime_id, payload.seat_id)
    return BookingResponse.model_validate(booking)


@router.get("/me", response_model=BookingListResponse, operation_id="list_my_bookings")
def list_my_bookings(
    service: BookingServiceDependency,
    user_id: CurrentUserId,
) -> BookingListResponse:
    bookings = service.list_my_bookings(user_id)
    return BookingListResponse(
        items=[BookingDetailsResponse.model_validate(item) for item in bookings]
    )


@router.get(
    "/{booking_id}",
    response_model=BookingDetailsResponse,
    operation_id="get_booking_details",
)
def get_booking_details(
    service: BookingServiceDependency,
    user_id: CurrentUserId,
    booking_id: Annotated[int, Path(ge=1)],
) -> BookingDetailsResponse:
    booking = service.get_booking_details(booking_id, user_id)
    return BookingDetailsResponse.model_validate(booking)


@router.delete(
    "/{booking_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    operation_id="cancel_booking",
)
def cancel_booking(
    service: BookingServiceDependency,
    user_id: CurrentUserId,
    booking_id: Annotated[int, Path(ge=1)],
) -> Response:
    service.cancel_booking(booking_id, user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
