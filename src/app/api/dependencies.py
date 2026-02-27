"""FastAPI dependency injection factories."""

from typing import Annotated

from fastapi import Depends

from app.application.user_service import UserService
from app.domain.uow import AbstractUnitOfWork
from app.infrastructure.uow import SqlAlchemyUnitOfWork


async def get_uow() -> AbstractUnitOfWork:
    """Provide a Unit of Work instance."""
    return SqlAlchemyUnitOfWork()


def get_user_service(
    uow: Annotated[AbstractUnitOfWork, Depends(get_uow)],
) -> UserService:
    """Provide a UserService wired with its dependencies."""
    return UserService(uow=uow)
