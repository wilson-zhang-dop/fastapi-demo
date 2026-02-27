"""Pydantic schemas for the User API."""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ── Request schemas ───────────────────────────────────────────────────


class UserCreate(BaseModel):
    """Schema for creating a new user."""

    email: EmailStr
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=128)
    full_name: str = Field(default="", max_length=128)


class UserUpdate(BaseModel):
    """Schema for updating an existing user."""

    username: str | None = Field(default=None, min_length=3, max_length=50)
    full_name: str | None = Field(default=None, max_length=128)


# ── Response schemas ──────────────────────────────────────────────────


class UserRead(BaseModel):
    """Schema for returning user data."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: str
    username: str
    full_name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


class PaginatedResponse(BaseModel):
    """Generic paginated response wrapper."""

    items: list[UserRead]
    total: int
    offset: int
    limit: int
    has_more: bool
