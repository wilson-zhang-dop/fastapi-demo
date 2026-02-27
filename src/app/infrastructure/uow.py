"""SQLAlchemy-based Unit of Work implementation."""

from types import TracebackType

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import async_session_factory
from app.domain.uow import AbstractUnitOfWork
from app.infrastructure.persistence.user_repository import SqlAlchemyUserRepository


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    """Concrete Unit of Work backed by an async SQLAlchemy session."""

    def __init__(self) -> None:
        self._session_factory = async_session_factory

    async def __aenter__(self) -> "SqlAlchemyUnitOfWork":
        self._session: AsyncSession = self._session_factory()
        self.users = SqlAlchemyUserRepository(self._session)
        return self  # type: ignore[return-value]

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await super().__aexit__(exc_type, exc_val, exc_tb)
        await self._session.close()

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()
