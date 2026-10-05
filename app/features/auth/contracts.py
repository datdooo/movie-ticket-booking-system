from typing import Protocol

from app.domain.entities import User


class UserRepository(Protocol):
    def get_by_email(self, email: str) -> User | None: ...

    def add(self, email: str, password_hash: str) -> User: ...
