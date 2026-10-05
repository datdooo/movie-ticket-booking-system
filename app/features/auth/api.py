from fastapi import APIRouter, status

from app.features.auth.dependencies import AuthServiceDependency
from app.features.auth.schemas import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    operation_id="register_user",
)
def register(payload: RegisterRequest, service: AuthServiceDependency) -> UserResponse:
    user = service.register(str(payload.email), payload.password)
    return UserResponse.model_validate(user)


@router.post("/login", response_model=TokenResponse, operation_id="login_user")
def login(payload: LoginRequest, service: AuthServiceDependency) -> TokenResponse:
    access_token = service.login(str(payload.email), payload.password)
    return TokenResponse(access_token=access_token)
