"""Test long running task tracking."""
import datetime
import time

import pytest
from tblib import Traceback

from top.longrunning.decorator import initialize, track
from top.redis.tracker import RedisTracker
from top.longrunning.task import LongRunningTask


@pytest.fixture()
def tracker(test_db_redis_url) -> RedisTracker:
    """Create default emitter"""
    emitter = RedisTracker.create_default_instance(
        LongRunningTask,
        redis_url=test_db_redis_url,
        max_past_tasks=50)
    emitter.clear()
    return emitter


@pytest.fixture()
def init(tracker):
    initialize(tracker)


def test_track_long_running(tracker: RedisTracker, init):
    """Track a long running task."""

    with track("simple"):
        time.sleep(1)

    time.sleep(0.050)  # Redis sync

    past_tasks = tracker.get_completed_tasks()
    assert len(past_tasks) == 1

    t = past_tasks[0]
    assert t.task_id is not None
    assert t.task_name == "simple"
    assert t.get_duration() > datetime.timedelta(seconds=1)
    assert t.traceback is None
    assert t.exception_message is None


def test_track_long_running_nested(tracker: RedisTracker, init):
    """Track nested running tasks."""

    with track("parent", task_id=1):
        with track("child", task_id=2):
            time.sleep(1)

    time.sleep(0.050)  # Redis sync

    past_tasks = tracker.get_completed_tasks()
    assert len(past_tasks) == 2

    t = past_tasks[0]
    assert t.task_id == 1
    assert t.task_name == "parent"
    assert t.get_duration() > datetime.timedelta(seconds=1)

    t = past_tasks[1]
    assert t.task_id == 2
    assert t.task_name == "child"
    assert t.get_duration() > datetime.timedelta(seconds=1)


def test_track_two(tracker: RedisTracker, init):
    """Track two tasks with the same name."""

    with track("simple"):
        time.sleep(0.25)

    with track("simple"):
        time.sleep(.25)

    time.sleep(0.050)  # Redis sync

    past_tasks = tracker.get_completed_tasks()
    assert len(past_tasks) == 2

    t = past_tasks[0]
    assert t.task_name == "simple"

    t = past_tasks[1]
    assert t.task_name == "simple"


def test_track_exception(tracker: RedisTracker, init):
    """Track a long running task."""

    with pytest.raises(RuntimeError):
        with track("simple"):
            raise RuntimeError("Hohoho")

    time.sleep(0.050)  # Redis sync

    past_tasks = tracker.get_completed_tasks()
    assert len(past_tasks) == 1

    t = past_tasks[0]
    assert t.task_id is not None
    assert t.task_name == "simple"
    assert t.exception_message == "Hohoho"

    # Check we can deserialise the traceback
    assert t.traceback is not None
    Traceback.from_dict(t.traceback)
