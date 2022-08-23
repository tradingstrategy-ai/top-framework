"""Entry points for integrations."""
import os
from typing import Type, Optional

from top.core.task import Task
from top.core.tracker import Tracker
from top.redis.tracker import RedisTracker


class NoTrackerAvailableException(Exception):
    """No tracker backend configured."""


def get_tracker_by_url_config(task_type: Type[Task], url: Optional[str]=None) -> Tracker:
    """Resolve tracker by its configuration URL.

    Reads `TOP_TRACKER_URL` and `TOP_MAX_COMPLETED_TASKS`
    environment variables.

    Currently only `redis://` supported.

    :param url:
        The URL that defines connection to the tracker backend.
        If not given use `TOP_TRACKER_URL` env.

    :param task_type:
        Subclass of Task or Task class itself.
        Used to serialise/deserialise data to Redis.
    """

    if not url:
        url = os.environ.get("TOP_TRACKER_URL")
        if not url:
            raise NoTrackerAvailableException(f"Tracker backend configuration URL missing TOP_TRACKER_URL missing.\nPlease refer to manual how to pass a tracker backend URL.")

    assert url.startswith("redis://"), f"Only Redis supported, got {url}"

    return RedisTracker.create_default_instance(task_type)
