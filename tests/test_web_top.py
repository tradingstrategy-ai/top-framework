"""Test web-top app."""

import pytest
from typer.testing import CliRunner

from top.redis.tracker import RedisTracker
from top.web.main import app
from top.web.task import HTTPTask


runner = CliRunner()


@pytest.fixture
def tracker() -> RedisTracker:
    """Create default emitter"""
    emitter = RedisTracker.create_default_instance(HTTPTask, max_past_tasks=50)
    emitter.clear()
    return emitter


def test_recent(tracker: RedisTracker):
    """Print recernt tasks to console."""

    t = HTTPTask.create_from_current_thread(1)
    tracker.start_task(t)
    tracker.end_task(t)

    t2 = HTTPTask.create_from_current_thread(2)
    tracker.start_task(t2)

    result = runner.invoke(app, ["recent"])
    assert result.exit_code == 0

