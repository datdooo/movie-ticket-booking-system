from typing import Annotated

from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.domain.errors import UnauthorizedError

bearer_scheme = HTTPBearer(auto_error=False)


def require_authenticated_user(
    request: Request,
    _: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
) -> None:
    if getattr(request.state, "current_user_id", None) is None:
        raise UnauthorizedError(
            code="UNAUTHORIZED",
            message="Thiếu token, token sai hoặc token đã hết hạn",
        )


def current_user_id(request: Request) -> int:
    user_id = getattr(request.state, "current_user_id", None)
    if user_id is None:
        raise UnauthorizedError(
            code="UNAUTHORIZED",
            message="Thiếu token, token sai hoặc token đã hết hạn",
        )
    return int(user_id)
