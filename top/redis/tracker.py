"""Redis based task storage backend."""

import datetime
import os
from typing import Dict, List, Type, Optional

from redis import StrictRedis, ConnectionPool

from top.core.tracker import Tracker
from top.core.task import Task


DEFAULT_MAX_COMPLETED_TASKS = 50


class RedisTracker(Tracker):
    """Manage task status in Redis.

    - Tasks are stored as UTF-8 encoded JSON blobs in Redis

    - Internally uses `redis-py <https://redis-py.readthedocs.io/en/stable/index.html>`_

    - It is recommended to give its own database for task tracking;
      do not share other databases (even though this works in theory)

    How to start tracking a (web) task:

    .. code-block:: python

            task_id = id(req)
            task = HTTPTask.create_from_current_thread(
                task_id,
                path=req.path,
                method=req.method,
                processor_name=str(worker),
                request_headers=req.headers,
            )
            tracker.start_task(task)

    Example how to finish a (web) task:

    .. code-block:: python

        task.status_code = resp.status_code
        task.status_message = resp.status
        task.response_headers = resp.headers

        tracker.end_task(task)
    """

    def __init__(self,
                 redis: StrictRedis,
                 task_type: Type[Task],
                 max_past_tasks=50):
        """Create a new emitter.

        :param redis:
            Redis instance

        :param task_type:
            Subclass of Task or Task class itself.
            Used to serialise/deserialise data to Redis.

        :param max_past_tasks:
            How many tasks to keep in the past events log
        """
        self.redis = redis

        self.task_type = task_type

        self.max_past_tasks = max_past_tasks

        #: Redis HSET, maps processor -> current task
        self.processors_hkey = "processors"

        #: Redis LIST, maps past tasks, the latest task on right
        self.past_tasks_list = "past_tasks"

        #: Pub sub key for task updates
        self.task_updates_channel = "task_updates"

        #: When we cleared the tracker last time
        self.last_cleared_at_key = "last_cleared_at"

    def clear(self):
        """Clear out whatever Redis database we are connected do.

        - Call at the restart of your system e.g. web server
          to clear any dangling processors

        - Call at the start of the tests when you need to clear
          the previous test database
        """
        for key in (self.processors_hkey, self.past_tasks_list,):
            self.redis.delete(key)

        # Add a marker key about clearing the database
        self.redis.set(self.last_cleared_at_key, datetime.datetime.now(datetime.timezone.utc).isoformat())

    def update_task(self, task: Task):
        task.updated_at = datetime.datetime.now(datetime.timezone.utc)
        processor_id = task.get_processor_tracking_id()
        data = task.serialise()

        # Update the task for the current processor
        self.redis.hset(self.processors_hkey, processor_id, data)

        # Do a notification on update
        self.redis.publish(self.task_updates_channel, data)

    def start_task(self, task: Task):
        self.update_task(task)

    def end_task(self, task: Task):
        task.ended_at = task.updated_at = datetime.datetime.now(datetime.timezone.utc)
        task.recorded_successfully = True

        data = task.serialise()

        # Delete task from the active processor
        processor_id = task.get_processor_tracking_id()
        self.redis.hdel(self.processors_hkey, processor_id)

        # Do a notification on update
        self.redis.publish(self.task_updates_channel, data)

        # Add task to the past buffer
        # https://stackoverflow.com/a/57776359/315168
        self.redis.lpush(self.past_tasks_list, data)
        self.redis.ltrim(self.past_tasks_list, 0, self.max_past_tasks - 1)

    def get_active_tasks(self) -> Dict[str, Task]:
        # Iterate over all hset keys and decode them as tasks.
        res = {}
        keys = self.redis.hkeys(self.processors_hkey)
        for processor_id in keys:
            task_blob = self.redis.hget(self.processors_hkey, processor_id)
            if task_blob is not None:
                # Because of race condition, we might have the key
                # gone missing while iterating
                res[processor_id] = self.task_type.deserialise(task_blob)
        return res

    def get_completed_tasks(self) -> List[Task]:
        res = []
        task_blobs = self.redis.lrange(self.past_tasks_list, 0, -1)
        for blob in task_blobs:
            res.append(self.task_type.deserialise(blob))
        return res

    @staticmethod
    def create_default_instance(task_type: Type[Task],
                                redis_url: Optional[str] = None,
                                redis_url_env="TOP_TRACKER_URL",
                                max_past_tasks_env="TOP_MAX_COMPLETED_TASKS",
                                max_past_tasks=None) -> "RedisTracker":
        """Creates a connection to the Redis database.

        :param task_type:
            Subclass of Task or Task class itself.
            Used to serialise/deserialise data to Redis.

        :param redis_url:
            Redis database string where to connect to

        :param redis_url_env:
            This environment variable contains the Redis URL where to connect

        :param max_past_tasks:
            How many tasks to keep in the past events log.
            If not given read `max_past_tasks_env` environment variable.
            If not available default to :py:data:`DEFAULT_MAX_COMPLETED_TASKS`.
        """

        if not redis_url:
            redis_url = os.environ.get(redis_url_env)
            if not redis_url:
                raise RuntimeError(f"You must configure Redis connection URL with {redis_url_env} environment variable")

        if not max_past_tasks:
            max_past_tasks = os.environ.get(max_past_tasks_env)
            if not max_past_tasks:
                max_past_tasks = DEFAULT_MAX_COMPLETED_TASKS
            else:
                max_past_tasks = int(max_past_tasks)

        pool = ConnectionPool.from_url(redis_url)
        client = StrictRedis(connection_pool=pool)

        return RedisTracker(client, task_type, max_past_tasks)
