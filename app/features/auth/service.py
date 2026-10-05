from app.domain.entities import User
from app.domain.errors import FeatureNotReadyError
from app.features.auth.contracts import UserRepository


class AuthService:
    """Business layer. This module must never import FastAPI or SQLAlchemy."""

    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def register(self, email: str, password: str) -> User:
        raise FeatureNotReadyError(
            code="AUTH_FEATURE_NOT_READY",
            message="Thành viên phụ trách auth cần triển khai AuthService.register",
        )

    def login(self, email: str, password: str) -> str:
        raise FeatureNotReadyError(
            code="AUTH_FEATURE_NOT_READY",
            message="Thành viên phụ trách auth cần triển khai AuthService.login",
        )
