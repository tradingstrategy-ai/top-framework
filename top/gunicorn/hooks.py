"""Gunicorn integration for web-top.

This module provides hooks you can refer in Gunicorn config.

See `Gunicorn settings <https://docs.gunicorn.org/en/stable/settings.html>`_
"""

from gunicorn.http import Request
from gunicorn.http.wsgi import Response
from gunicorn.workers.base import Worker

from top.integration import get_tracker_by_url_config
from top.utils import is_sphinx_build
from top.web.task import HTTPTask


#: A global initialisation per worker, etc.
#: Not sure if gunicorn offers us a smarter approach to do this,
#: e.g. by worker?
if not is_sphinx_build():
    tracker = get_tracker_by_url_config(HTTPTask)
else:
    # Don't crash the docs build
    tracker = None


def when_ready(server):
    """Called when the web server restarts."""
    tracker.clear()


def pre_request(worker: Worker, req: Request):
    """Gunicorn pre_request hook."""

    task_id = id(req)
    task = HTTPTask.create_from_current_thread(
        task_id,
        path=req.path,
        method=req.method,
        processor_name=str(worker),
        request_headers=req.headers,
        client_ip_address=str(req.peer_addr[0]),  # ip, port tuple
    )
    tracker.start_task(task)

    req.tracked_task = task


def post_request(worker: Worker, req: Request, environ: dict, resp: Response):
    """Gunicorn post_request hook."""
    task: HTTPTask = getattr(req, "tracked_task", None)
    assert task is not None, "Request did not carry tracking information"

    task.status_code = resp.status_code
    task.status_message = resp.status
    task.response_headers = resp.headers

    tracker.end_task(task)
