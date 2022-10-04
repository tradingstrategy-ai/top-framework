from dataclasses import dataclass
from typing import Optional

from dataclasses_json import dataclass_json

from top.core.task import Task


@dataclass_json
@dataclass
class LongRunningTask(Task):
    """A task class for background and long-running tasks."""

    #: If the task faile with Python exception, contain the pickled traceback
    #:
    #: Serialised to nested dicts with tblib that are JSON compatible.
    #: https://pypi.org/project/tblib/
    traceback: Optional[dict] = None

    #: If the task failed with Python exception, contain the Exception message
    #:
    exception_message: Optional[str] = None