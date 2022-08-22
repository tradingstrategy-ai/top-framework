"""Test redis backend."""

import datetime
import time

import pytest

from top.core.task import Task
from top.redis.tracker import RedisTracker


@pytest.fixture
def tracker() -> RedisTracker:
    """Create default emitter"""
    emitter = RedisTracker.create_default_instance(max_past_tasks=50)
    emitter.clear()
    return emitter


def test_start_end_task(tracker: RedisTracker):
    """Push a new task and read it back."""

    t = Task.create_from_current_thread("1")
    tracker.start_task(t)
    time.sleep(0.50)

    # Check the task appears in the current tasks
    current_tasks = tracker.get_active_tasks()
    t2 = next(iter(current_tasks.values()))
    assert t2.task_id == t.task_id
    assert t2.started_at > datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)
    assert t2.updated_at > datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)
    assert t2.ended_at is None

    past_tasks = tracker.get_completed_tasks()
    assert len(past_tasks) == 0

    # Finish the task and see it is cleaned up
    tracker.end_task(t)
    time.sleep(0.50)

    current_tasks = tracker.get_active_tasks()
    assert len(current_tasks) == 0

    past_tasks = tracker.get_completed_tasks()
    assert len(past_tasks) == 1

    t3 = past_tasks[0]
    assert t3.ended_at > datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)
    assert t3.ended_at > t3.started_at
    assert t3.ended_at == t3.updated_at
    assert t3.recorded_successfully


def test_past_task_order(tracker: RedisTracker):
    """Make sure past events come through in the right order."""

    t1 = Task.create_from_current_thread(1)
    t2 = Task.create_from_current_thread(2)
    t3 = Task.create_from_current_thread(3)

    tracker.start_task(t1)
    tracker.start_task(t2)
    tracker.start_task(t3)

    # Then close in different order
    tracker.end_task(t2)
    completed_tasks = tracker.get_completed_tasks()
    assert completed_tasks[0].task_id == t2.task_id

    tracker.end_task(t3)
    completed_tasks = tracker.get_completed_tasks()
    assert completed_tasks[0].task_id == t3.task_id
    assert completed_tasks[1].task_id == t2.task_id

    tracker.end_task(t1)
    completed_tasks = tracker.get_completed_tasks()
    assert completed_tasks[0].task_id == t1.task_id
    assert completed_tasks[1].task_id == t3.task_id
    assert completed_tasks[2].task_id == t2.task_id


def test_past_overflow(tracker: RedisTracker):
    """Push more tasks than our past task log can handle."""

    tasks = []
    for i in range(1, 60):
        t = Task.create_from_current_thread(i)
        tracker.start_task(t)
        tasks.append(t)

    # Finish tasks from 1 to 60
    for t in tasks:
        tracker.end_task(t)

    completed_tasks = tracker.get_completed_tasks()
    assert len(completed_tasks) == 50

    assert completed_tasks[0].task_id == 59

