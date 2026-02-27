"""Abstract repository interface for User aggregate."""

from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.user.entity import User


class AbstractUserRepository(ABC):
    """Port / interface for User persistence."""

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> User | None: ...

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None: ...

    @abstractmethod
    async def get_by_username(self, username: str) -> User | None: ...

    @abstractmethod
    async def list(
        self,
        *,
        offset: int = 0,
        limit: int = 20,
        is_active: bool | None = None,
    ) -> list[User]: ...

    @abstractmethod
    async def count(self, *, is_active: bool | None = None) -> int: ...

    @abstractmethod
    async def add(self, user: User) -> User: ...

    @abstractmethod
    async def update(self, user: User) -> User: ...

    @abstractmethod
    async def delete(self, user_id: UUID) -> None: ...
