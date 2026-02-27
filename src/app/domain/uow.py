"""Abstract Unit of Work interface."""

from abc import ABC, abstractmethod
from types import TracebackType

from app.domain.user.repository import AbstractUserRepository


class AbstractUnitOfWork(ABC):
    """Port for transactional consistency.

    Usage::

        async with uow:
            user = await uow.users.get_by_id(uid)
            user.deactivate()
            await uow.users.update(user)
            await uow.commit()
    """

    users: AbstractUserRepository

    async def __aenter__(self) -> "AbstractUnitOfWork":
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if exc_type is not None:
            await self.rollback()

    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def rollback(self) -> None: ...
