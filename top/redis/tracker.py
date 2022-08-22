"""Redis based task storage backend."""

import datetime
import os
from typing import Dict, Set, List, Type

from redis import StrictRedis, ConnectionPool

from top.core.tracker import Tracker
from top.core.task import Task


class RedisTracker(Tracker):
    """Manage task status in Redis.

    - Internally uses `redis-py <https://redis-py.readthedocs.io/en/stable/index.html>`_

    - It is recommended to give its own database for task tracking;
      do not share other databases (even though this works in theory)
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

    def clear(self):
        """Clear out whatever Redis dataabase we are connected do.

        - Call at the restart of your system e.g. web server
          to clear any dangling processors

        - Call at the start of the tests when you need to clear
          the previous test database
        """
        for key in (self.processors_hkey, self.past_tasks_list,):
            self.redis.delete(key)

    def update_task(self, task: Task):
        task.updated_at = datetime.datetime.utcnow()
        processor_id = task.get_processor_tracking_id()
        data = task.serialise()

        # Update the task for the current processor
        self.redis.hset(self.processors_hkey, processor_id, data)

        # Do a notification on update
        self.redis.publish(self.task_updates_channel, data)

    def start_task(self, task: Task):
        self.update_task(task)

    def end_task(self, task: Task):
        task.ended_at = task.updated_at = datetime.datetime.utcnow()
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
        """Iterate over all hset keys and decode them as tasks.

        :param cls:
            Subclass of Task that is used to deserialise data.
        """
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
                                env_var_name="TOP_REDIS_URL",
                                max_past_tasks=50) -> "RedisTracker":
        """Creates a connection to the Redis database.

        :param task_type:
            Subclass of Task or Task class itself.
            Used to serialise/deserialise data to Redis.

        :param env_var_name:
            This environment variable contains the Redis URL where to connect

        :param max_past_tasks:
            How many tasks to keep in the past events log
        """

        redis_url = os.environ.get(env_var_name)
        if not redis_url:
            raise RuntimeError(f"You must configure Redis connection URL with {env_var_name} environment variable")

        pool = ConnectionPool.from_url(redis_url)
        client = StrictRedis(connection_pool=pool)

        return RedisTracker(client, task_type, max_past_tasks)
