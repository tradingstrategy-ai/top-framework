
from dataclasses import dataclass
from typing import Optional, List, Tuple, Dict

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

    #: The full request URI if available
    uri: Optional[str] = None

    #: Client IP address
    client_ip_address: Optional[str] = None

    #: Request HTTP headers.
    #:
    #: Available as key value mapping.
    #:
    #: Note that in HTTP protocol a header can appear twice.
    #:
    #: Uppercase all key names.
    #:
    request_headers: Optional[List[Tuple[str, str]]] = None

    #: When response has been generated, what code did we sent.
    #: Only available when the request processing has finished.
    status_code: Optional[int] = None

    #: Server status message
    status_message: Optional[str] = None

    #: Response HTTP headers.
    #:
    #: Available as key value mapping.
    #:
    #: Note that in HTTP protocol a header can appear twice.
    #: Uppercase all key names.
    #:
    response_headers: Optional[List[Tuple[str, str]]] = None

    def __repr__(self):
        if self.params:
            params = " ".join([f"{key}={value}" for key, value in self.params.items()])
        else:
            params = """"""
        if self.status_code:
            return f"<HTTPTask {self.method} {self.path} {params} {self.status_code}>"
        else:
            return f"<HTTPTask {self.method} {self.path} {params}>"

    def get_single_request_header(self, name: str) -> Optional[str]:
        """Get a value of a single HTTP header in a request.

        :param name:
            Case insensitive HTTP header name

        :raise AssertionError:
            If the same header appears twice

        :return:
            The header value
        """

        if not self.request_headers:
            return None

        retval = None
        for header, value in self.request_headers:
            if header.upper() == name.upper():
                assert not retval, "The header appears twice: {name}"
                retval = value

        return retval

    def get_single_response_header(self, name: str) -> Optional[str]:
        """Get a value of a single HTTP header in a response.

        :param name:
            Case insensitive HTTP header name

        :raise AssertionError:
            If the same header appears twice

        :return:
            The header value
        """

        if not self.response_headers:
            return None

        retval = None
        for header, value in self.response_headers:
            if header.upper() == name.upper():
                assert not retval, "The header appears twice: {name}"
                retval = value

        return retval

    def get_host(self) -> str:
        """HTTP request header shortcut method."""
        return self.get_single_request_header("HOST")

    def get_user_agent(self) -> str:
        """HTTP request header shortcut method."""
        return self.get_single_request_header("USER-AGENT")

    def get_accept_encoding(self) -> str:
        """HTTP request header shortcut method."""
        return self.get_single_request_header("ACCEPT-ENCODING")

    def get_content_length(self) -> Optional[int]:
        """Get the content length of the response.

        If not set return None.
        """
        val = self.get_single_response_header("Content-length")
        if val:
            return int(val)
        return None
