
from dataclasses import dataclass
from typing import Optional

from dataclasses_json import dataclass_json

from top.core.task import Task


@dataclass_json
@dataclass
class HTTPTask(Task):
    """A task for tracking HTTP requests."""

    #: HTTP method like GET, POST, put
    method: str

    #: /api/my-func
    path: str

    #: HTTP headers dumped as a dict
    headers: dict

    #: When response has been generated, what code did we sent
    status_code: Optional[int] = None

    #: When response has been generated, what status text we sent
    status_text: Optional[int] = None





