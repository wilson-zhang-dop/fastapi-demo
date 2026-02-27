"""Shared test fixtures."""

import asyncio
from collections.abc import AsyncGenerator, Generator
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app.api.dependencies import get_uow
from app.domain.uow import AbstractUnitOfWork
from app.domain.user.entity import User
from app.main import create_app


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create a single event loop for the test session."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


def _make_fake_user(**overrides) -> User:  # noqa: ANN003
    defaults = {
        "id": uuid4(),
        "email": "test@example.com",
        "username": "testuser",
        "hashed_password": "hashed",
        "full_name": "Test User",
        "is_active": True,
    }
    defaults.update(overrides)
    return User(**defaults)


class FakeUserRepository:
    """In-memory user repository for testing."""

    def __init__(self, users: list[User] | None = None) -> None:
        self._store: dict[str, User] = {}
        for u in users or []:
            self._store[str(u.id)] = u

    async def get_by_id(self, user_id):  # noqa: ANN001, ANN201
        return self._store.get(str(user_id))

    async def get_by_email(self, email: str) -> User | None:
        return next((u for u in self._store.values() if u.email == email), None)

    async def get_by_username(self, username: str) -> User | None:
        return next((u for u in self._store.values() if u.username == username), None)

    async def list(self, *, offset=0, limit=20, is_active=None):  # noqa: ANN001, ANN201
        items = list(self._store.values())
        if is_active is not None:
            items = [u for u in items if u.is_active == is_active]
        return items[offset : offset + limit]

    async def count(self, *, is_active=None) -> int:  # noqa: ANN001
        items = list(self._store.values())
        if is_active is not None:
            items = [u for u in items if u.is_active == is_active]
        return len(items)

    async def add(self, user: User) -> User:
        self._store[str(user.id)] = user
        return user

    async def update(self, user: User) -> User:
        self._store[str(user.id)] = user
        return user

    async def delete(self, user_id) -> None:  # noqa: ANN001
        self._store.pop(str(user_id), None)


class FakeUnitOfWork(AbstractUnitOfWork):
    """In-memory Unit of Work for testing."""

    def __init__(self, users: list[User] | None = None) -> None:
        self.users = FakeUserRepository(users)
        self.committed = False

    async def __aenter__(self):  # noqa: ANN204
        return self

    async def __aexit__(self, *args):  # noqa: ANN002, ANN204
        pass

    async def commit(self) -> None:
        self.committed = True

    async def rollback(self) -> None:
        pass


@pytest_asyncio.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """Provide an async HTTP client backed by the FastAPI app with fake deps."""
    fake_uow = FakeUnitOfWork(users=[_make_fake_user()])

    app = create_app()
    app.dependency_overrides[get_uow] = lambda: fake_uow

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
