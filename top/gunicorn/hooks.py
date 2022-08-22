"""Gunicorn hooks.

See `Gunicorn settings <https://docs.gunicorn.org/en/stable/settings.html>`_
"""

from gunicorn.http import Request
from gunicorn.http.wsgi import Response
from gunicorn.workers.base import Worker

from top.integration import get_tracker_by_url_config
from top.web.task import HTTPTask


tracker = get_tracker_by_url_config(HTTPTask)


def when_ready(server):
    """Called when the web server restarts."""
    tracker.clear()


def pre_request(worker: Worker, req: Request):
    """Gunicorn pre_request hook."""
    worker.log.debug("%s %s" % (req.method, req.path))


def post_request(worker: Worker, req: Request, environ: dict, resp: Response):
    """Gunicorn post_request hook."""
    worker.log.debug("%s %s: %d" % (req.method, req.path, resp.status_code))