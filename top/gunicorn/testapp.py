"""A sample Gunicorn test application that does nothing.

Used in integration tests.

`From Gunicorn documentation <https://docs.gunicorn.org/en/stable/run.html>`_.
"""
import itertools
import random
import time

from lorem import paragraph


def app(environ, start_response):
    """Simplest possible application object"""
    data = b'Hello, World!\n'
    status = '200 OK'
    response_headers = [
        ('Content-type', 'text/plain'),
        ('Content-Length', str(len(data)))
    ]
    start_response(status, response_headers)
    return iter([data])


def slow_app(environ, start_response):
    """Simple test app with delays"""

    text = "\n".join(list(itertools.islice(paragraph(), 3)))
    data = text.encode("utf-8")

    statuses = [
        "200 OK",
        "302 Moved temporarily",
        "404 Not found",
        "500 Internal server error",
    ]

    status = random.choice(statuses)
    response_headers = [
        ('Content-type', 'text/plain; charset=utf8'),
        ('Content-Length', str(len(data)))
    ]
    time.sleep(random.uniform(0.1, 2))
    start_response(status, response_headers)
    return iter([data])
