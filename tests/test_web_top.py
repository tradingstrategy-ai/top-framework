"""Test web-top app."""

import pytest
from typer.testing import CliRunner

from top.redis.tracker import RedisTracker
from top.tui.column import determine_enabled_columns
from top.web.column import http_task_column_mappings
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
        http_task_column_mappings,
        [t]
    )
    assert columns == ['Cty', 'IP']

    # Now without header
    t: HTTPTask = HTTPTask.create_from_current_thread(1)
    assert t.get_ip_country() is None
    columns = ["Cty", "IP"]
    columns = determine_enabled_columns(
        columns,
        http_task_column_mappings,
        [t]
    )
    assert columns == ['IP']
