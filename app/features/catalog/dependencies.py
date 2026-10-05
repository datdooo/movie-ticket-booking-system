from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db_session
from app.features.catalog.repository import SqlAlchemyCatalogRepository
from app.features.catalog.service import CatalogService


def get_catalog_service(session: Annotated[Session, Depends(get_db_session)]) -> CatalogService:
    return CatalogService(SqlAlchemyCatalogRepository(session))


CatalogServiceDependency = Annotated[CatalogService, Depends(get_catalog_service)]
