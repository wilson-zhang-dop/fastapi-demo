"""Unit tests for the User domain entity."""

import pytest

from app.core.exceptions import BusinessRuleViolationError
from app.domain.user.entity import User


def test_user_deactivate() -> None:
    user = User(email="a@b.com", username="abc", is_active=True)
    user.deactivate()
    assert user.is_active is False


def test_user_deactivate_already_inactive() -> None:
    user = User(email="a@b.com", username="abc", is_active=False)
    with pytest.raises(BusinessRuleViolationError):
        user.deactivate()


def test_user_activate() -> None:
    user = User(email="a@b.com", username="abc", is_active=False)
    user.activate()
    assert user.is_active is True


def test_user_update_profile_short_username() -> None:
    user = User(email="a@b.com", username="abc")
    with pytest.raises(BusinessRuleViolationError):
        user.update_profile(username="ab")
