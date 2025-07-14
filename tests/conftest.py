from unittest.mock import MagicMock

import pytest


@pytest.fixture
def session():
    """Mocked SQLModel session, no real DB."""
    return MagicMock()
