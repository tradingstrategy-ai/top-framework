import pytest


@pytest.fixture
def test_db_redis_url() -> str:
    """Redis DB URL for testing"""
    return "redis://localhost:7777/15"