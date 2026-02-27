"""User application service (use case layer)."""

from uuid import UUID

from app.core.exceptions import EntityAlreadyExistsError, EntityNotFoundError
from app.core.security import hash_password
from app.domain.uow import AbstractUnitOfWork
from app.domain.user.entity import User


class UserService:
    """Orchestrates user-related use cases."""

    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self._uow = uow

    # ── Queries ───────────────────────────────────────────────────────

    async def get_user(self, user_id: UUID) -> User:
        async with self._uow:
            user = await self._uow.users.get_by_id(user_id)
            if user is None:
                raise EntityNotFoundError("User", user_id)
            return user

    async def list_users(
        self,
        *,
        offset: int = 0,
        limit: int = 20,
        is_active: bool | None = None,
    ) -> tuple[list[User], int]:
        async with self._uow:
            users = await self._uow.users.list(offset=offset, limit=limit, is_active=is_active)
            total = await self._uow.users.count(is_active=is_active)
            return users, total

    # ── Commands ──────────────────────────────────────────────────────

    async def create_user(
        self,
        *,
        email: str,
        username: str,
        password: str,
        full_name: str = "",
    ) -> User:
        async with self._uow:
            if await self._uow.users.get_by_email(email):
                raise EntityAlreadyExistsError("User", "email", email)
            if await self._uow.users.get_by_username(username):
                raise EntityAlreadyExistsError("User", "username", username)

            user = User(
                email=email,
                username=username,
                hashed_password=hash_password(password),
                full_name=full_name,
            )
            created = await self._uow.users.add(user)
            await self._uow.commit()
            return created

    async def update_user(
        self,
        user_id: UUID,
        *,
        full_name: str | None = None,
        username: str | None = None,
    ) -> User:
        async with self._uow:
            user = await self._uow.users.get_by_id(user_id)
            if user is None:
                raise EntityNotFoundError("User", user_id)

            if username and username != user.username:
                existing = await self._uow.users.get_by_username(username)
                if existing:
                    raise EntityAlreadyExistsError("User", "username", username)

            user.update_profile(full_name=full_name, username=username)
            updated = await self._uow.users.update(user)
            await self._uow.commit()
            return updated

    async def deactivate_user(self, user_id: UUID) -> User:
        async with self._uow:
            user = await self._uow.users.get_by_id(user_id)
            if user is None:
                raise EntityNotFoundError("User", user_id)
            user.deactivate()
            updated = await self._uow.users.update(user)
            await self._uow.commit()
            return updated

    async def delete_user(self, user_id: UUID) -> None:
        async with self._uow:
            user = await self._uow.users.get_by_id(user_id)
            if user is None:
                raise EntityNotFoundError("User", user_id)
            await self._uow.users.delete(user_id)
            await self._uow.commit()
