from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.errors import ERROR_RESPONSES, register_exception_handlers
from app.api.middleware.authentication import AuthenticationMiddleware
from app.api.router import api_router
from app.core.config import get_settings
from app.db.session import init_db


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    init_db()
    yield


def create_app(*, initialize_database: bool = True) -> FastAPI:
    settings = get_settings()
    application = FastAPI(
        title=settings.app_name,
        version="1.0.0",
        description="Backend REST API cho nghiệp vụ đặt vé xem phim.",
        lifespan=lifespan if initialize_database else None,
        responses=ERROR_RESPONSES,
    )
    application.add_middleware(AuthenticationMiddleware, settings=settings)
    register_exception_handlers(application)

    @application.get("/health", tags=["technical"], operation_id="health_check")
    def health_check() -> dict[str, str]:
        return {"status": "ok"}

    application.include_router(api_router)
    return application


app = create_app()
