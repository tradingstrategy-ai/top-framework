"""Test redis backend."""

import datetime
import time

import pytest

from top.core.task import Task
from top.redis.tracker import RedisTracker


@pytest.fixture
def emitter() -> RedisTracker:
    """Create default emitter"""
    emitter = RedisTracker.create_default_instance()
    emitter.clear_dangerous()
    return emitter


def test_start_end_task(emitter: RedisTracker):
    """Push a new task and read it back."""

    t = Task.create_from_current_thread("1")
    emitter.start_task(t)
    time.sleep(0.50)

    # Check the task appears in the current tasks
    current_tasks = emitter.get_active_tasks()
    t2 = next(iter(current_tasks.values()))
    assert t2.task_id == t.task_id
    assert t2.started_at > datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)
    assert t2.updated_at > datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)
    assert t2.ended_at is None

    past_tasks = emitter.get_completed_tasks()
    assert len(past_tasks) == 0

    # Finish the task and see it is cleaned up
    emitter.end_task(t)
    time.sleep(0.50)

    current_tasks = emitter.get_active_tasks()
    assert len(current_tasks) == 0

    past_tasks = emitter.get_completed_tasks()
    assert len(past_tasks) == 1

    t3 = past_tasks[0]
    assert t3.ended_at > datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)
    assert t3.ended_at > t3.started_at
    assert t3.ended_at == t3.updated_at
    assert t3.recorded_successfully
