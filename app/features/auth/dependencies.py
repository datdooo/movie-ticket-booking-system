from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db_session
from app.features.auth.repository import SqlAlchemyUserRepository
from app.features.auth.service import AuthService


def get_auth_service(session: Annotated[Session, Depends(get_db_session)]) -> AuthService:
    return AuthService(SqlAlchemyUserRepository(session))


AuthServiceDependency = Annotated[AuthService, Depends(get_auth_service)]
