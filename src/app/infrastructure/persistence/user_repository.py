"""SQLAlchemy implementation of the User repository."""

from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.user.entity import User
from app.domain.user.repository import AbstractUserRepository
from app.infrastructure.persistence.user_model import UserModel


class SqlAlchemyUserRepository(AbstractUserRepository):
    """Concrete repository backed by PostgreSQL via async SQLAlchemy."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, user_id: UUID) -> User | None:
        result = await self._session.get(UserModel, user_id)
        return result.to_entity() if result else None

    async def get_by_email(self, email: str) -> User | None:
        stmt = select(UserModel).where(UserModel.email == email)
        result = await self._session.execute(stmt)
        row = result.scalar_one_or_none()
        return row.to_entity() if row else None

    async def get_by_username(self, username: str) -> User | None:
        stmt = select(UserModel).where(UserModel.username == username)
        result = await self._session.execute(stmt)
        row = result.scalar_one_or_none()
        return row.to_entity() if row else None

    async def list(
        self,
        *,
        offset: int = 0,
        limit: int = 20,
        is_active: bool | None = None,
    ) -> list[User]:
        stmt = select(UserModel).offset(offset).limit(limit).order_by(UserModel.created_at.desc())
        if is_active is not None:
            stmt = stmt.where(UserModel.is_active == is_active)
        result = await self._session.execute(stmt)
        return [row.to_entity() for row in result.scalars()]

    async def count(self, *, is_active: bool | None = None) -> int:
        stmt = select(func.count()).select_from(UserModel)
        if is_active is not None:
            stmt = stmt.where(UserModel.is_active == is_active)
        result = await self._session.execute(stmt)
        return result.scalar_one()

    async def add(self, user: User) -> User:
        model = UserModel.from_entity(user)
        self._session.add(model)
        await self._session.flush()
        return model.to_entity()

    async def update(self, user: User) -> User:
        model = await self._session.get(UserModel, user.id)
        if model is None:
            raise ValueError(f"User {user.id} does not exist")
        model.email = user.email
        model.username = user.username
        model.hashed_password = user.hashed_password
        model.full_name = user.full_name
        model.is_active = user.is_active
        model.updated_at = user.updated_at
        await self._session.flush()
        return model.to_entity()

    async def delete(self, user_id: UUID) -> None:
        model = await self._session.get(UserModel, user_id)
        if model:
            await self._session.delete(model)
            await self._session.flush()
