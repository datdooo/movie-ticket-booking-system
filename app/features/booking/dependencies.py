from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db_session
from app.features.booking.repository import SqlAlchemyBookingRepository
from app.features.booking.service import BookingService


def get_booking_service(session: Annotated[Session, Depends(get_db_session)]) -> BookingService:
    return BookingService(SqlAlchemyBookingRepository(session))


BookingServiceDependency = Annotated[BookingService, Depends(get_booking_service)]
