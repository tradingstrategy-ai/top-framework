"""Web server based REST API backend integration."""

import enum
import os
from typing import Dict, List, Type, Optional, Union

import requests

from top.core.tracker import Tracker
from top.core.task import Task


class RESTResponseException(Exception):
    """Something for with REST API response"""
    pass


class Actions(enum.Enum):
    """What actions our REST API endpoint provides.

    See https://github.com/tradingstrategy-ai/web-top-node/blob/master/src/server.ts
    """
    active_tasks = "active-tasks"
    completed_tasks = "completed-tasks"


class RESTAPITracker(Tracker):
    """REST API integration for getting active HTTP requests from a web server.

    Get active and completed requests from the web server direclty.

    - You have a web server that itself can track its active requests and completed responses

    - The web server implements Top Framework REST API for fetching the tasks

    - Used with `Node.js integration <https://www.npmjs.com/package/@trading-strategy-ai/web-top-node>`_
    """

    def __init__(self,
                 api_url: str,
                 task_type: Type[Task],
                 api_key: Optional[str] = None,
                 ):
        """Create a new emitter.

        :param api_url:
            Tracked endpoint at the web server.

            Usually `/tracker`.

        :param api_key:
            The API key needed to access the tracker endpoint.

            If not set read from `TOP_WEB_API_KEY` environment variable.

        :param task_type:
            A custom serialisation/deserialisation class for the data.
        """
        self.task_type = task_type

        self.api_url = api_url

        if api_key:
            self.api_key = api_key
        else:
            self.api_key = os.environ.get("TOP_WEB_API_KEY")
            if not self.api_key:
                raise RuntimeError(f"You must configure Tracker API endpoint key with TOP_WEB_API_KEY environment variable")

        # HTTP 1.1 keep alive connection
        self.session = requests.Session()

    def clear(self):
        raise NotImplementedError("Must be provided by the server integration")

    def start_task(self, task: Task):
        raise NotImplementedError("Must be provided by the server integration")

    def end_task(self, task: Task):
        raise NotImplementedError("Must be provided by the server integration")

    def get_active_tasks(self) -> Dict[Union[int, str], Task]:
        resp = self.session.get(
            self.api_url,
            params={
                "api-key": self.api_key,
                "action": Actions.active_tasks.value,
            }
        )

        if resp.status_code != 200:
            raise RESTResponseException(f"Could not read the response: {self.api_url}: {resp.text}")

        raw_data = resp.json()
        return {key: self.task_type.from_dict(value) for key, value in raw_data.items()}

    def get_completed_tasks(self) -> List[Task]:
        resp = self.session.get(
            self.api_url,
            params={
                "api-key": self.api_key,
                "action": Actions.completed_tasks.value,
            }
        )

        if resp.status_code != 200:
            raise RESTResponseException(f"Could not read the response: {self.api_url}: {resp.text}")

        raw_data = resp.json()
        return [self.task_type.from_dict(item) for item in raw_data]
