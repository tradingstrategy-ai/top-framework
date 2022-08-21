"""Task core structure definition."""

import datetime
import os
import threading
from dataclasses import dataclass
from typing import Optional, Union

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Task:
    """A generic structure for tracking tasks across processors.

    All fields are optional for maximum flexibility.

    `dataclasses_json library <https://github.com/lidatong/dataclasses-json>`_ is used to automatically
    convert Python :py:mod:`dataclass` structures to JSON and back.
    """

    #: UNIX process that started this task
    process_id: Optional[int] = None

    #: UNIX thread that started this task
    thread_id: Optional[int] = None

    #: If the application provides further ids for the processes.
    #: E.g. connection id in PostgreSQL
    process_internal_id: Optional[str] = None

    #: E.g. web request id if available.
    #: Depends on the application.
    #: Can be int or str depending on the context.
    task_id: Optional[Union[int, str]] = None

    #: Human readable of the processor name is available
    processor_name: Optional[str] = None

    #: When this task was started.
    #: UTC timestamp, naive (no timezone).
    #: Automatically filled by :py:meth:`create_from_current_thread`.
    started_at: Optional[datetime.datetime] = None

    #: When this task was startead
    #: UTC timestamp, naive (no timezone)
    updated_at: Optional[datetime.datetime] = None

    #: When this task was ended.
    #: Automatically filled by :py:meth:`top.core.tracker.Tracker.end_task`.
    ended_at: Optional[datetime.datetime] = None

    #: Did this task success?
    #:
    #: None = we do not know yet.
    #: true = task received its end_task() call.
    #: false = task was cleaned up by monitor/timeout.
    recorded_successfully: Optional[bool] = None

    def __eq__(self, other: "Task"):
        """All tasks are identified by their task_id attribute.
        """
        return self.task_id == other.task_id

    def __hash__(self):
        """Allows easily create index (hash map) of all tasks."""
        return hash((self.task_id))

    def get_processor_tracking_id(self) -> str:
        """Get the key used in our tracking table (Redis) for this task."""
        return f"{self.process_id}-{self.thread_id}-{self.process_internal_id}"

    def serialise(self) -> bytes:
        """Serialise using dataclasS_json"""
        return self.to_json().encode("utf-8")

    @staticmethod
    def deserialise(blob: bytes) -> "Task":
        """Serialise using dataclasses_json"""
        return Task.from_json(blob)

    @staticmethod
    def create_from_current_thread(task_id: Union[str, int], **kwargs) -> "Task":
        """Create a task and assuming the processor is the current OS thread.

        Automatically labels the task to belong to the OS
        current process/thread.

        :param task_id:
            Something unique to identify this task.
            If nothing else then use Python object hash.

        :param kwargs:
            Passed to :py:class:`Task` dataclass constructor.

        """

        pid = os.getpid()
        tid = threading.get_ident()

        thread_name = threading.current_thread().name
        processor_name = f"{pid}:{thread_name}" or kwargs.get("processor_name")

        return Task(
            task_id=task_id,
            process_id=pid,
            thread_id=tid,
            started_at=datetime.datetime.utcnow(),
            processor_name=processor_name,
            **kwargs,
        )

