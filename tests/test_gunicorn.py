"""Gunicorn integration tests.

References

- https://github.com/ConsenSys/python-utils/blob/9725f15f688303e116b7937242f8354a4a070808/tests/gunicorn/test_app.py

"""
import datetime
import shutil
import subprocess
import time

import psutil
import pytest
import requests


from top.redis.tracker import RedisTracker
from top.utils import is_localhost_port_listening
from top.web.task import HTTPTask


@pytest.fixture
def tracker(test_db_redis_url) -> RedisTracker:
    """Create default emitter"""
    emitter = RedisTracker.create_default_instance(
        HTTPTask,
        redis_url=test_db_redis_url,
    )
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

    assert not is_localhost_port_listening(port), f"Port {port} already reserved - do we have zombie gunicorn around? try pkill -f gunicorn"

    gunicorn_binary = "gunicorn"

    found = shutil.which(gunicorn_binary)
    if not found:
        raise RuntimeError(f"Could not find gunicorn binary: {gunicorn_binary} - are you sure it is installed?")

    cmd_list = [
        "gunicorn",
        f"--bind=127.0.0.1:{port}",
        "--workers=2",
        "--config=scripts/gunicorn-example-config.py",
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

    process.terminate()

    # Dump Gunicorn logs
    # TODO: Make this conditional and only do if the test fails
    stdout = process.communicate()[0].decode("utf-8")
    stderr = process.communicate()[1].decode("utf-8")
    print(stdout)
    print(stderr)


def test_gunicorn_request(tracker: RedisTracker, server: str):
    """Test that we get a request through."""
    resp = requests.get(server)
    assert resp.status_code == 200


def test_cleared(tracker: RedisTracker, server: str):
    """Clear tracker database on startup."""
    redis = tracker.redis
    cleared_val = redis.get(tracker.last_cleared_at_key).decode("utf-8")
    cleared_at = datetime.datetime.fromisoformat(cleared_val)
    assert datetime.datetime.now(datetime.timezone.utc) - cleared_at < datetime.timedelta(seconds=10)


def test_track_gunicorn(tracker: RedisTracker, server: str):
    """Check that we track a request."""

    assert len(tracker.get_completed_tasks()) == 0

    resp = requests.get(server)
    assert resp.status_code == 200

    # Give Redis time to sync
    time.sleep(0.100)

    assert len(tracker.get_active_tasks()) == 0
    assert len(tracker.get_completed_tasks()) == 1

    task: HTTPTask = tracker.get_completed_tasks()[0]

    assert task.status_code == 200
    assert task.status_message == "200 OK"
    assert task.path == "/"
    assert task.get_ago() > datetime.timedelta(0)
    assert task.get_duration() > datetime.timedelta(0)

    assert task.get_host() == "localhost:9999"
    assert task.get_accept_encoding() == "gzip, deflate"
    assert task.get_user_agent().startswith("python-requests/")
    assert task.client_ip_address == "127.0.0.1"

    assert task.get_content_length() == 14


def test_track_path(tracker: RedisTracker, server: str):
    """Check we get path tracked correctly."""

    assert len(tracker.get_completed_tasks()) == 0

    resp = requests.get(f"{server}/folder")
    assert resp.status_code == 200

    # Give Redis time to sync
    time.sleep(0.100)

    task: HTTPTask = tracker.get_completed_tasks()[0]

    assert task.path == "/folder"


def test_track_multiple(tracker: RedisTracker, server: str):
    """Check multiple requests get tracked correctly."""

    assert len(tracker.get_completed_tasks()) == 0

    requests.get(f"{server}/1")
    requests.get(f"{server}/2")
    requests.get(f"{server}/3")

    # Give Redis time to sync
    time.sleep(0.100)

    assert len(tracker.get_completed_tasks()) == 3
