import json
import os

import pytest
from pyramid.config import Configurator
from pyramid.request import Request
from pyramid.view import view_config
from webtest.http import StopableWSGIServer

from top.restapi.tracker import Actions, RESTAPITracker
from top.web.task import HTTPTask


EXAMPLE_TASK_DATA = json.loads("""
{"task_id":1,"protocol":null,"host":null,"method":"GET","path":"/foobar","params":{"action":"active-tasks"},"tags":{"node.platform":"darwin","node.version":"v16.15.0"},"client_ip_address":"::1","request_headers":[["HOST","localhost:3000"],["CONNECTION","keep-alive"],["CACHE-CONTROL","max-age=0"],["SEC-CH-UA","\"Chromium\";v=\"104\", \" Not A;Brand\";v=\"99\", \"Google Chrome\";v=\"104\""],["SEC-CH-UA-MOBILE","?0"],["SEC-CH-UA-PLATFORM","\"macOS\""],["UPGRADE-INSECURE-REQUESTS","1"],["USER-AGENT","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"],["ACCEPT","text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"],["SEC-FETCH-SITE","none"],["SEC-FETCH-MODE","navigate"],["SEC-FETCH-USER","?1"],["SEC-FETCH-DEST","document"],["ACCEPT-ENCODING","gzip, deflate, br"],["ACCEPT-LANGUAGE","en-US,en;q=0.9"]],"process_id":49492,"host_name":"ilwrath.local","updated_at":"2022-08-29T10:10:44.734Z","started_at":"2022-08-29T10:10:44.734Z"}
""")


EXAMPLE_API_KEY = "123"


@view_config(renderer="json")
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
        config.add_view(dummy_tracker, route_name='dummy_tracker')
        app = config.make_wsgi_app()
        return app


@pytest.fixture
def server(app):
    """Test web server"""
    server = StopableWSGIServer(app)
    server.wait()
    yield "http://localhost:3456"
    server.shutdown()


def test_rest_active_tasks(server):
    """RESTAPITracker.get_active_tasks works"""
    os.environ["WEB_TOP_API_KEY"] = EXAMPLE_API_KEY
    tracker_url = f"{server}/tracker"
    tracker = RESTAPITracker(tracker_url, task_type=HTTPTask)
    active = tracker.get_active_tasks()
    assert len(active) == 1
