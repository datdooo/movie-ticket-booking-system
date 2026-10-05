from sqlalchemy.orm import Session

from app.domain.entities import User
from app.domain.errors import FeatureNotReadyError


class SqlAlchemyUserRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_email(self, email: str) -> User | None:
        raise FeatureNotReadyError(
            code="AUTH_REPOSITORY_NOT_READY",
            message="Triển khai truy vấn user theo email trong feature/auth/repository.py",
        )

    def add(self, email: str, password_hash: str) -> User:
        raise FeatureNotReadyError(
            code="AUTH_REPOSITORY_NOT_READY",
            message="Triển khai tạo user trong feature/auth/repository.py",
        )
