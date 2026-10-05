from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import Settings
from app.core.security import TokenError, decode_access_token


class AuthenticationMiddleware(BaseHTTPMiddleware):
    """Decode Bearer tokens once and expose the user id through request.state."""

    def __init__(self, app: object, settings: Settings) -> None:
        super().__init__(app)
        self.settings = settings

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        request.state.current_user_id = None
        authorization = request.headers.get("Authorization")

        if authorization:
            scheme, _, token = authorization.partition(" ")
            if scheme.lower() != "bearer" or not token:
                return _unauthorized_response()
            try:
                request.state.current_user_id = decode_access_token(token, self.settings)
            except TokenError:
                return _unauthorized_response()

        return await call_next(request)


def _unauthorized_response() -> JSONResponse:
    return JSONResponse(
        status_code=401,
        content={
            "error": {
                "code": "UNAUTHORIZED",
                "message": "Thiếu token, token sai hoặc token đã hết hạn",
            }
        },
        headers={"WWW-Authenticate": "Bearer"},
    )
