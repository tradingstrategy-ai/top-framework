import json
import os

import pytest
from pyramid.config import Configurator
from pyramid.request import Request
from pyramid.view import view_config
from webtest.http import StopableWSGIServer

from top.restapi.tracker import Actions, RESTAPITracker
from top.web.task import HTTPTask


# Load some random output data to simulate web-top API output
EXAMPLE_FILE = os.path.join(os.path.dirname(__file__), "sample.json")

EXAMPLE_TASK_DATA = json.load(open(EXAMPLE_FILE, "rt"))

EXAMPLE_API_KEY = "123"


def dummy_tracker(request: Request):
    """Endpoint to simulate web-top-node"""
    assert request.method == "GET"
    api_key = request.params["api-key"]
    assert api_key == EXAMPLE_API_KEY
    action = request.params["action"]
    if action == Actions.active_tasks.value:
        return {1: EXAMPLE_TASK_DATA}
    if action == Actions.completed_tasks.value:
        return [EXAMPLE_TASK_DATA]
    else:
        raise RuntimeError("No")


@pytest.fixture
def test_app():
    """WSGI app to simulate web-top-node"""
    with Configurator() as config:
        config.add_route('dummy_tracker', '/tracker')
        config.add_view(dummy_tracker, route_name='dummy_tracker', renderer='json')
        app = config.make_wsgi_app()
        return app


@pytest.fixture
def server(test_app):
    """Test web server"""
    server = StopableWSGIServer.create(test_app, port=3333)
    server.wait(retries=1)
    yield "http://localhost:3333"
    server.shutdown()


def test_rest_active_tasks(server):
    """RESTAPITracker.get_active_tasks works"""
    # Test reading API key from the environment variable
    os.environ["TOP_WEB_API_KEY"] = EXAMPLE_API_KEY
    tracker_url = f"{server}/tracker"
    tracker = RESTAPITracker(tracker_url, task_type=HTTPTask)
    active = tracker.get_active_tasks()
    assert len(active) == 1

    assert active["1"]["started_at"] != None
    assert active["1"]["task_id"] == 1


def test_rest_completed_tasks(server):
    """RESTAPITracker.get_active_tasks works"""
    # Test reading API key from the environment variable
    os.environ["TOP_WEB_API_KEY"] = EXAMPLE_API_KEY
    tracker_url = f"{server}/tracker"
    tracker = RESTAPITracker(tracker_url, task_type=HTTPTask)
    completed = tracker.get_completed_tasks()
    assert len(completed) == 1
    assert completed[0]["started_at"] != None
    assert completed[0]["task_id"] == 1
