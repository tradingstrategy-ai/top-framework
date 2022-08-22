"""Gunicorn integration tests.

References

- https://github.com/ConsenSys/python-utils/blob/9725f15f688303e116b7937242f8354a4a070808/tests/gunicorn/test_app.py

-
"""
import shutil
import subprocess
import time

import psutil
import pytest
import requests

from top.core.task import Task
from top.redis.tracker import RedisTracker
from top.utils import is_localhost_port_listening


@pytest.fixture
def tracker() -> RedisTracker:
    """Create default emitter"""
    emitter = RedisTracker.create_default_instance(Task)
    emitter.clear()
    return emitter


@pytest.fixture
def server() -> str:
    """Launch Gunicorn integration test server using command line.

    - Start a test instance of Gunicorn in a child process

    - Listen to in port 9999.

    :yield:
        The test server URL when up
    """

    port = 9999
    start_timeout = 3.0

    assert not is_localhost_port_listening(port)

    gunicorn_binary = "gunicorn"

    found = shutil.which(gunicorn_binary)
    if not found:
        raise RuntimeError(f"Could not find gunicorn binary: {gunicorn_binary} - are you sure it is installed?")

    cmd_list = [
        "gunicorn",
        f"--bind=127.0.0.1:{port}",
        "--workers=2",
        "top.gunicorn.testapp:app"
    ]

    out = subprocess.PIPE
    process = psutil.Popen(cmd_list, stdin=subprocess.DEVNULL, stdout=out, stderr=out)

    # Check that gunicorn starts in the port we want
    deadline = time.time() + start_timeout
    while time.time() < deadline:
        if is_localhost_port_listening(port):
            break

    if time.time() > deadline:
        # Dump Gunicorn stderr startup logs to terminal
        if process.poll() is not None:
            stdout = process.communicate()[0].decode("utf-8")
            stderr = process.communicate()[1].decode("utf-8")
            raise RuntimeError(f"Failed to launch gunicorn:\n{stdout}\n{stderr}")

    yield f"http://localhost:{port}"
    process.kill()


def test_gunicorn_request(tracker: RedisTracker, server: str):
    """Test that we get a request through."""

    print("Making a request")
    resp = requests.get(server)
    assert resp.status_code == 200
