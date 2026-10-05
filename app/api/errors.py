from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.exceptions import HTTPException

from app.domain.errors import (
    AppError,
    ConflictError,
    FeatureNotReadyError,
    ForbiddenError,
    NotFoundError,
    RuleViolationError,
    UnauthorizedError,
)

STATUS_BY_ERROR_TYPE = {
    ConflictError: 409,
    ForbiddenError: 403,
    NotFoundError: 404,
    RuleViolationError: 400,
    UnauthorizedError: 401,
    FeatureNotReadyError: 501,
}


class ErrorBody(BaseModel):
    code: str
    message: str


class ErrorResponse(BaseModel):
    error: ErrorBody


ERROR_RESPONSES = {
    code: {"model": ErrorResponse} for code in (400, 401, 403, 404, 405, 409, 422, 500, 501)
}


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(HTTPException)
    async def handle_http_error(_: Request, exc: HTTPException) -> JSONResponse:
        code = {404: "NOT_FOUND", 405: "METHOD_NOT_ALLOWED"}.get(exc.status_code, "HTTP_ERROR")
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": {"code": code, "message": str(exc.detail)}},
            headers=exc.headers,
        )

    @app.exception_handler(Exception)
    async def handle_unexpected_error(_: Request, __: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content={"error": {"code": "INTERNAL_ERROR", "message": "Lỗi hệ thống"}},
        )

    @app.exception_handler(AppError)
    async def handle_app_error(_: Request, exc: AppError) -> JSONResponse:
        status_code = STATUS_BY_ERROR_TYPE.get(type(exc), 400)
        headers = {"WWW-Authenticate": "Bearer"} if status_code == 401 else None
        return JSONResponse(
            status_code=status_code,
            content={"error": {"code": exc.code, "message": exc.message}},
            headers=headers,
        )

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(_: Request, __: RequestValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content={
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Dữ liệu đầu vào không hợp lệ",
                }
            },
        )
