
from dataclasses import dataclass
from typing import Optional

from dataclasses_json import dataclass_json

from top.core.task import Task


@dataclass_json
@dataclass
class HTTPTask(Task):
    """A task for tracking HTTP requests."""

    #: HTTP method like GET, POST, put
    method: Optional[str] = None

    #: Request path, like /api/my-func
    path: Optional[str] = None

    #: HTTP GET request params
    params: Optional[dict] = None

    #: Request HTTP headers dumped as a dict.
    request_headers: Optional[dict] = None

    #: When response has been generated, what code did we sent.
    #: Only available when the request processing has finished.
    status_code: Optional[int] = None

    #: Server status message
    status_message: Optional[str] = None

    #: Response HTTP headers dumped as a dict.
    response_headers: Optional[dict] = None

    def __repr__(self):
        if self.params:
            params = " ".join([f"{key}={value}" for key, value in self.params.items()])
        else:
            params = """"""
        if self.response_status_code:
            return f"<{self.method} {self.path} {params} {self.response_status_code}>"
        else:
            return f"<{self.method} {self.path} {params}>"
