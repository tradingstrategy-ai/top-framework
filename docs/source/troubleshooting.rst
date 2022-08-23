Troubleshooting
===============

View raw Redis content
----------------------

Connect to Redis and inspect what is going on in the tracker database.

When using Docker, assuming database number 15,
start `redis-cli`:

.. code-block:: shell

     docker exec -it redis redis-cli --raw --pass $REDIS_PASSWORD -n 15

Then you can browse the database using `redis-cli`:

.. code-block::

    127.0.0.1:6379[15]> keys *
    1) "last_cleared_at"
    2) "processors"
    3) "past_tasks"


Show last 3 tasks:

.. code-block::

    lrange past_tasks 0 2

This will output the raw JSON records:

.. code-block::

    {"process_id": 2125131, "thread_id": 140539531953920, "process_internal_id": null, "task_id": 140538974609616, "processor_name": "<Worker 2125131>", "started_at": "2022-08-23T15:49:10.905607+00:00", "updated_at": "2022-08-23T15:49:11.631117+00:00", "ended_at": "2022-08-23T15:49:11.631117+00:00", "recorded_successfully": true, "tags": null, "method": "GET", "path": "/api/candles", "params": null, "uri": null, "client_ip_address": "127.0.0.1", "request_headers": [["HOST", "tradingstrategy.ai"], ["USER-AGENT", "python-requests/2.27.1"], ["ACCEPT", "*/*"], ["ACCEPT-ENCODING", "gzip"], ["CDN-LOOP", "cloudflare"], ["CF-CONNECTING-IP", "xx"], ["CF-IPCOUNTRY", "US"], ["CF-RAY", "73f4ff26be5e8226-IAD"], ["CF-VISITOR", "{\"scheme\":\"https\"}"], ["CONTENT-TYPE", "application/json"], ["X-FORWARDED-FOR", "xx, yy"], ["X-FORWARDED-PROTO", "https"]], "status_code": 200, "status_message": "200 OK", "response_headers": [["Content-Type", "application/json"], ["Content-Length", "429000"], ["Access-Control-Allow-Origin", "*"], ["Access-Control-Allow-Methods", "POST,GET,DELETE,PUT,OPTIONS"], ["Access-Control-Allow-Headers", "Origin, Content-Type, Accept, Authorization"], ["Access-Control-Allow-Credentials", "true"], ["Access-Control-Max-Age", "1728000"]]}

Force reinstall package for Poetry
----------------------------------

Poetry does not know how to check for the latest commit.
Do:

.. code-block:: shell

    pip install --force-reinstall --no-deps "https://github.com/tradingstrategy-ai/top-framework.git#master"