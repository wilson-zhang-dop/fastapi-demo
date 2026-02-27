"""User domain entity (aggregate root)."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone

from app.core.exceptions import BusinessRuleViolationError


@dataclass
class User:
    """User aggregate root.

    Encapsulates business rules and invariants for the User concept.
    """

    id: uuid.UUID = field(default_factory=uuid.uuid4)
    email: str = ""
    username: str = ""
    hashed_password: str = ""
    full_name: str = ""
    is_active: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    # ── Business rules ────────────────────────────────────────────────

    def deactivate(self) -> None:
        if not self.is_active:
            raise BusinessRuleViolationError("User is already deactivated")
        self.is_active = False
        self._touch()

    def activate(self) -> None:
        if self.is_active:
            raise BusinessRuleViolationError("User is already active")
        self.is_active = True
        self._touch()

    def update_profile(self, full_name: str | None = None, username: str | None = None) -> None:
        if full_name is not None:
            self.full_name = full_name
        if username is not None:
            if len(username) < 3:
                raise BusinessRuleViolationError(
                    "Username must be at least 3 characters"
                )
            self.username = username
        self._touch()

    # ── Helpers ───────────────────────────────────────────────────────

    def _touch(self) -> None:
        self.updated_at = datetime.now(timezone.utc)
