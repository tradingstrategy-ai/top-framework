"""Task core structure definition."""

import datetime
import os
import socket
import sys
import threading
from dataclasses import dataclass, field
from typing import Optional, Union, List

from dataclasses_json import dataclass_json, config
from marshmallow import fields

from top.core.encoding import encode_date, decode_date


@dataclass_json
@dataclass
class Task:
    """A generic structure for tracking tasks across workers.

    All fields are optional for maximum flexibility.

    `dataclasses_json library <https://github.com/lidatong/dataclasses-json>`_ is used to automatically
    convert Python :py:mod:`dataclasses` structures to JSON and back.
    """

    #: Unique identified for this task.
    #:
    #: E.g. web request id if available.
    #: Depends on the application.
    #: Can be int or str depending on the context.
    #:
    task_id: Optional[Union[int, str]] = None

    #: Unique identified for the parent task in a nested task hierarchy.
    #:
    #: Needed e.g. when doing subprocess trees.
    #:
    parent_task_id: Optional[Union[int, str]] = None

    #: Human readable name for this task.
    #:
    #: From cron-like jobs this can be the cron job name.
    #: For :py:class:`~top.core.web.task.HTTPTask`
    #: this is not set, but tasks are identified by URI that consists of
    #  protocol, host,
    #: :py:data:`~top.core.web.task.HTTPTask.method` and :py:data:`~top.core.web.task.HTTPTask.path`.
    task_name: Optional[str] = None

    #: Host name on multiserver deployments.
    #:
    #: E.g. the web server DNS name if multiple
    #: servers behind a load balancer.
    host_name: Optional[str] = None

    #: OS process id that started this task.
    #:
    process_id: Optional[int] = None

    #: OS thread that started this task.
    #:
    thread_id: Optional[int] = None

    #: If the application provides further ids for the processes.
    #:
    #: E.g. connection id in PostgreSQL
    process_internal_id: Optional[str] = None

    #: Human readable of the processor name is available
    processor_name: Optional[str] = None

    #: When this task was started.
    #:
    #: UTC timestamp serialised as ISO 8601.
    #: Automatically filled by :py:meth:`create_from_current_thread`.
    started_at: Optional[datetime.datetime] = field(
        default=None,
        metadata=config(
            encoder=encode_date,
            decoder=decode_date,
            mm_field=fields.DateTime(format='iso')
        )
    )
    #: When this task was last updated.
    #:
    #: UTC timestamp serialised as ISO 8601.
    updated_at: Optional[datetime.datetime] = field(
        default=None,
        metadata=config(
            encoder=encode_date,
            decoder=decode_date,
            mm_field=fields.DateTime(format='iso')
        )
    )

    #: When this task was ended.
    #:
    #: UTC timestamp serialised as ISO 8601.
    #: Automatically filled by :py:meth:`top.core.tracker.Tracker.end_task`.
    ended_at: Optional[datetime.datetime] = field(
        default=None,
        metadata=config(
            encoder=encode_date,
            decoder=decode_date,
            mm_field=fields.DateTime(format='iso')
        )
    )
    #: Did this task success?
    #:
    #: None = we do not know yet.
    #: True = task received its end_task() call.
    #: False = task was cleaned up by monitor/timeout.
    recorded_successfully: Optional[bool] = None

    #: Generic tracking tags that can be associated with tasks.
    #:
    #: Frameworks like `OpenTelemetry <https://opentelemetry.io/>`__
    #: and statsd support tagging sources and events.
    #: Usually these are used to detect the server production mode,
    #: deployed version,
    #: Kubernetes/Docker/other deployment information and such,
    #:
    #: Here you can add any tags to the request.
    #: When :py:meth:`top.core.tracker.Tracker.start_task`
    #: is called, the tracker specific tags are automatically
    #: applied here.
    #:
    #: - `See OpenTelemetry specification <https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/common/README.md#attribute>`_
    #:
    #: - `See some example OpenTelemetry attributes and labels <https://lightstep.com/opentelemetry/attributes-and-labels>`_
    #:
    tags: Optional[dict] = None

    #: Application command line
    #:
    #: Space separated command that was used to start this process.
    #: Same as sys.argv.
    #:
    command_line: Optional[List[str]] = None

    def __eq__(self, other: "Task"):
        """All tasks are identified by their task_id attribute.
        """
        return self.task_id == other.task_id

    def __hash__(self):
        """Allows easily create index (hash map) of all tasks."""
        return hash((self.task_id))

    def get_processor_tracking_id(self) -> str:
        """Get the key used in our tracking table (Redis) for this task.

        You can also override this function to have specific processor id
        scheme for your application.
        """
        if self.process_internal_id:
            return f"{self.process_id}-{self.thread_id}-{self.process_internal_id}"
        else:
            return f"pid:{self.process_id} tid:{self.thread_id}"

    def get_duration(self) -> Optional[datetime.timedelta]:
        """Get the duration of this task.

        - For completed tasks, return the actual duration

        - For active tasks, return how much time has passed since start

        - If start is missing, return None
        """

        if self.started_at:
            if self.ended_at:
                return self.ended_at - self.started_at
            else:
                return datetime.datetime.now(datetime.timezone.utc) - self.started_at

        return None

    def get_ago(self) -> Optional[datetime.timedelta]:
        """Get how long ago this task finished.

        :return:
            Relative to now, or None if the task is not yet finished
        """
        if self.ended_at:
            return datetime.datetime.now(datetime.timezone.utc) - self.ended_at
        return None

    def serialise(self) -> bytes:
        """Serialise using dataclasS_json"""
        blob = self.to_json().encode("utf-8")
        return blob

    @classmethod
    def deserialise(cls, blob: bytes) -> "Task":
        """Serialise using dataclasses_json"""
        return cls.from_json(blob)

    @classmethod
    def create_from_current_thread(cls,
                                   task_id: Union[str, int],
                                   processor_name: Optional[str] = None,
                                   **kwargs) -> "Task":
        """Create a task and assuming the processor is the current OS thread.

        Automatically labels the task to belong to the OS
        current process/thread. This will fill the following fields:

        - :py:attr:`process_id`

        - :py:attr:`thread_id`

        - :py:attr:`processor_name`

        - :py:attr:`host_name` (`socket.gethostname()`)

        - Command line (`sys.argv`)

        :param task_id:
            Something unique to identify this task.
            If nothing else then use Python object hash.

        :param processor_name:
            Framework specific name for this processor

        :param kwargs:
            Passed to :py:class:`Task` dataclass constructor.

        """

        pid = os.getpid()
        tid = threading.get_ident()

        thread_name = threading.current_thread().name

        # https://stackoverflow.com/a/49610911/315168
        host_name = socket.gethostname()

        if not processor_name:
            processor_name = f"{pid}:{thread_name}"

        return cls(
            task_id=task_id,
            process_id=pid,
            thread_id=tid,
            host_name=host_name,
            started_at=datetime.datetime.now(datetime.timezone.utc),
            processor_name=processor_name,
            command_line=sys.argv,
            **kwargs,
        )
