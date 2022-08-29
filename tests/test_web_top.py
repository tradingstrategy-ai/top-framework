"""Test web-top app."""

import pytest
from typer.testing import CliRunner

from top.redis.tracker import RedisTracker
from top.tui.column import determine_enabled_columns

from top.web.main import app
from top.web.task import HTTPTask
from top.web.web_columns import http_task_columns


runner = CliRunner()


@pytest.fixture
def tracker(test_db_redis_url) -> RedisTracker:
    """Create default emitter"""
    emitter = RedisTracker.create_default_instance(
        HTTPTask,
        redis_url=test_db_redis_url,
        max_past_tasks=50)
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


def test_dynamic_country_rule(tracker: RedisTracker):
    """Check if the dynamic country column rule works."""

    t: HTTPTask = HTTPTask.create_from_current_thread(1)
    t.request_headers = [
        ("CF-IPCountry", "FI")
    ]
    assert t.get_ip_country() is not None
    columns = ["Cty", "IP"]
    columns = determine_enabled_columns(
        columns,
        http_task_columns,
        [t]
    )
    assert columns == ['Cty', 'IP']

    # Now without header
    t: HTTPTask = HTTPTask.create_from_current_thread(1)
    assert t.get_ip_country() is None
    columns = ["Cty", "IP"]
    columns = determine_enabled_columns(
        columns,
        http_task_columns,
        [t]
    )
    assert columns == ['IP']


def test_x_forwarded_for():
    """Check if the dynamic country column rule works."""

    t: HTTPTask = HTTPTask.create_from_current_thread(1)
    t.request_headers = [
        ("X-Forwarded-for", "1.1.1.1, 8.8.8.8")
    ]
    assert t.get_original_ip() == "1.1.1.1"
