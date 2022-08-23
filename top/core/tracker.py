"""Task tracking core."""

import abc
from typing import Dict, List

from top.core.task import Task


class Tracker(abc.ABC):
    """Task tracker backend interface definition."""

    @abc.abstractmethod
    def clear(self):
        """Clear the tracker from old/dangling tasks.

        For example if the server has

        - Crashed

        - Restarted

        Get rid of any stale data.

        Can be called on the web server start.
        """

    @abc.abstractmethod
    def start_task(self, task: Task):
        """Start a new task.

        Record a task started in the tracker backend.
        """

    @abc.abstractmethod
    def end_task(self, task: Task):
        """Finish exisiting task.

        Mark task completed.
        """

    @abc.abstractmethod
    def get_active_tasks(self) -> Dict[str, Task]:
        """Get currently active tasks.

        :return:
            Map of (Processor id -> Task)
        """

    @abc.abstractmethod
    def get_completed_tasks(self) -> List[Task]:
        """Get the backlog of completed tasks.

        Each backend can have N number of tasks in a ring buffer
        that are last completed.

        Tasks are in the completion order.
        The most recently completed task is the first item in the list.

        :return:
            List of past completed tasks that are in our past tasks buffer.
            The most recently completed task is the first item in the list.
        """