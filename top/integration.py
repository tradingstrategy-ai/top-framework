"""Entry points for integrations."""
import os
from typing import Type, Optional

from top.core.task import Task
from top.core.tracker import Tracker
from top.redis.tracker import RedisTracker
from top.restapi.tracker import RESTAPITracker


class NoTrackerAvailableException(Exception):
    """No tracker backend configured."""


def get_tracker_by_url_config(
        task_type: Type[Task],
        url: Optional[str] = None,
        api_key: Optional[str] = None,
) -> Optional[Tracker]:
    """Resolve tracker by its configuration URL.

    Reads `TOP_TRACKER_URL` and `TOP_MAX_COMPLETED_TASKS`
    environment variables.

    Currently only `redis://` supported.

    Because this code is run during Python module import,
    we will detect conditions based on environment variables
    like `READTHEDOCS` to allow us to shortcut the logic
    and not try to create tracker connection during docs
    build.

    :param url:
        The URL that defines connection to the tracker backend.
        If not given use `TOP_TRACKER_URL` env.

    :param task_type:
        Subclass of Task or Task class itself.
        Used to serialise/deserialise data to Redis.

    :param api_key:
        API key for REST web server integration.
        If not given read from `TOP_WEB_API_KEY`
        environment variable.

    :return:
        A new task Tracker, unless we are under a special
        build environment.
    """

    # https://docs.readthedocs.io/en/stable/environment-variables.html
    if os.environ.get("READTHEDOCS") or os.environ.get("SPHINX_BUILD"):
        return None

    if not url:
        url = os.environ.get("TOP_TRACKER_URL")
        if not url:
            raise NoTrackerAvailableException("Tracker backend configuration URL missing TOP_TRACKER_URL missing.\nPlease refer to manual how to pass a tracker backend URL.")

    if url.startswith("redis://"):
        assert url.startswith("redis://"), f"Only Redis supported, got {url}"
        return RedisTracker.create_default_instance(task_type, url)
    elif url.startswith("http://") or url.startswith("https://"):
        return RESTAPITracker(url, task_type, api_key=api_key)
    else:
        raise NoTrackerAvailableException(f"Does not recognise URL: {url}")
