"""Domain base entity."""

import uuid
from datetime import datetime, timezone


class BaseEntity:
    """Base class for all domain entities."""

    def __init__(self, id: uuid.UUID | None = None) -> None:
        self.id = id or uuid.uuid4()
        self.created_at: datetime = datetime.now(timezone.utc)
        self.updated_at: datetime = datetime.now(timezone.utc)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BaseEntity):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
