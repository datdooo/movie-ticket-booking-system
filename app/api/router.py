from fastapi import APIRouter

from app.features.auth.api import router as auth_router
from app.features.booking.api import router as booking_router
from app.features.catalog.api import router as catalog_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(catalog_router)
api_router.include_router(booking_router)
