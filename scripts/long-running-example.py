import time
import pprint

from top.redis.tracker import RedisTracker
from top.longrunning.task import LongRunningTask

from top.longrunning.decorator import initialize, track

# Configure Redis database #2 for task tracking
# in a Redis instance running at localhost:7777.
# See Redispy for more configuration instructions.
tracker = RedisTracker.create_default_instance(
    LongRunningTask,
    redis_url="redis://localhost:7777/2",
    max_past_tasks=1024)

initialize(tracker)

with track("parent"):
    time.sleep(0.25)
    with track("child"):
        time.sleep(0.25)

# You can use tracker instance in any Python
# script to print active or past tasks
past_tasks = tracker.get_completed_tasks()
pprint.pprint(past_tasks)