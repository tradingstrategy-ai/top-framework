"""Gunicorn hooks.

See `Gunicorn settings <https://docs.gunicorn.org/en/stable/settings.html>`_
"""

from gunicorn.http import Request
from gunicorn.http.wsgi import Response
from gunicorn.workers.base import Worker

from top.integration import get_tracker_by_url_config
from top.web.task import HTTPTask


#: A global initialisation per worker, etc.
#: Not sure if gunicorn offers us a smarter approach to do this,
#: e.g. by worker?
tracker = get_tracker_by_url_config(HTTPTask)


def when_ready(server):
    """Called when the web server restarts."""
    tracker.clear()


def pre_request(worker: Worker, req: Request):
    """Gunicorn pre_request hook."""
    worker.log.error("%s %s" % (req.method, req.path))

    task_id = id(req)
    task = HTTPTask.create_from_current_thread(
        task_id,
        path=req.path,
        method=req.method,
    )
    tracker.start_task(task)

    req.tracked_task = task


def post_request(worker: Worker, req: Request, environ: dict, resp: Response):
    """Gunicorn post_request hook."""
    task: HTTPTask = getattr(req, "tracked_task", None)
    assert task is not None, "Request did not carry tracking information"

    task.status_code = resp.status_code
    task.status_message = resp.status

    tracker.end_task(task)
