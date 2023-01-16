"""Simple task tracking implementation with a Python contextmanager.

This implementation is suitable for simple task tracking.

Pros

- Very simple, easy to understand and configure

Cons

- Cannot handle scalability, back pressure and such
"""
import sys
import threading
import uuid
from contextlib import AbstractContextManager, contextmanager
from typing import Any, Optional, List, Type

from tblib import Traceback

from top.core.tracker import Tracker
from top.longrunning.task import LongRunningTask


class NotInitialized(Exception):
    """initialize() not called."""


class LongRunningTaskContextManagerFactory:
    """A context manager factory to track long running tasks.

    - You need to hae one instance for each thread

    What an ugly class name. Let's Java.
    """

    def __init__(self, tracker: Tracker, TaskClass: Type[LongRunningTask] = LongRunningTask):
        self.tracker = tracker
        self.TaskClass = TaskClass

        # Allow nested tasks
        self.task_stack: List[LongRunningTask] = []

    @contextmanager
    def track(self, name: str, task_id: Optional[str] = None, **kwargs) -> AbstractContextManager[Any]:
        """Context manager factory."""

        if task_id is None:
            task_id = str(uuid.uuid1())

        if len(self.task_stack) > 0:
            parent_task_id = self.task_stack[-1].parent_task_id
        else:
            parent_task_id = None

        task = self.TaskClass.create_from_current_thread(task_id, parent_task_id=parent_task_id, **kwargs)

        task.task_name = name

        self.tracker.start_task(task)
        self.task_stack.append(task)

        try:
            yield
        except Exception as e:
            # https://pypi.org/project/tblib/#toc-entry-8
            et, ev, tb = sys.exc_info()
            tb = Traceback(tb)
            exception_message = str(e)
            task.traceback = tb.to_dict()
            task.exception_message = exception_message
            raise
        finally:
            self.tracker.end_task(task)
            self.task_stack.pop()


thread_storage = threading.local()


def initialize(tracker: Tracker):
    """ "Initialize tracker backend for the context manager.

    You must call this from each thread that tracks tasks.
    """
    global track
    thread_storage.track = LongRunningTaskContextManagerFactory(tracker)


@contextmanager
def track(*args, **kwargs):
    """The default context manager to track Python task duration.

    See :py:func:`initialize` how to initialize per thread.

    See :py:class:`LongRunningTaskContextManagerFactory` for instructions.
    """
    _track_impl = getattr(thread_storage, "track")

    if _track_impl is None:
        raise NotInitialized("Please call initialize() before calling track() for each thread where you are going to use this")

    with _track_impl.track(*args, **kwargs):
        yield
