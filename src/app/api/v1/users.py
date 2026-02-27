"""User API router."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.api.dependencies import get_user_service
from app.api.schemas import PaginatedResponse, UserCreate, UserRead, UserUpdate
from app.application.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])

UserServiceDep = Annotated[UserService, Depends(get_user_service)]


@router.get("", response_model=PaginatedResponse)
async def list_users(
    service: UserServiceDep,
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    is_active: bool | None = Query(default=None),
) -> PaginatedResponse:
    """List users with pagination and optional active-status filter."""
    users, total = await service.list_users(offset=offset, limit=limit, is_active=is_active)
    return PaginatedResponse(
        items=[UserRead.model_validate(u, from_attributes=True) for u in users],
        total=total,
        offset=offset,
        limit=limit,
        has_more=(offset + limit) < total,
    )


@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: UUID, service: UserServiceDep) -> UserRead:
    """Retrieve a single user by ID."""
    user = await service.get_user(user_id)
    return UserRead.model_validate(user, from_attributes=True)


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(body: UserCreate, service: UserServiceDep) -> UserRead:
    """Create a new user."""
    user = await service.create_user(
        email=body.email,
        username=body.username,
        password=body.password,
        full_name=body.full_name,
    )
    return UserRead.model_validate(user, from_attributes=True)


@router.patch("/{user_id}", response_model=UserRead)
async def update_user(user_id: UUID, body: UserUpdate, service: UserServiceDep) -> UserRead:
    """Partially update a user."""
    user = await service.update_user(
        user_id,
        full_name=body.full_name,
        username=body.username,
    )
    return UserRead.model_validate(user, from_attributes=True)


@router.post("/{user_id}/deactivate", response_model=UserRead)
async def deactivate_user(user_id: UUID, service: UserServiceDep) -> UserRead:
    """Deactivate a user account."""
    user = await service.deactivate_user(user_id)
    return UserRead.model_validate(user, from_attributes=True)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: UUID, service: UserServiceDep) -> None:
    """Permanently delete a user."""
    await service.delete_user(user_id)
