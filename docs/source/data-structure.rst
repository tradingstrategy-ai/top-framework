.. _data structure:

Data structure
==============

Preface
-------

Top framework provides a general data structure that allows you to
build your own `top`-like monitoring tools easily.

All data is serialised as JSON. JSON is easily writeable and readable by any application,
programming language or tool. The write protocol is writing JSON to any database/in-memory buffer.

Task providers and text user interface (TUI) applications communicate over a a tracker backend.

The default tracker backend is
Redis, but this is easily replaceable, because the interface
code is only few hundreds of lines of Python.
For OS `top` like process tracker you do not need a backend at all,
because you can get this information directly from your kernel.

Tracker backends
----------------

At the moment, we provide support for :ref:`Redis`.

Generic tasks and processors structure
--------------------------------------

See :py:class:`top.core.task.Task`.

The following data structure is used:

- Processor (pid + thread)
    - Each processor may have 0 or 1 activate tasks
    - Tracked in Redis HSET `processors`

- Current task
    - Task unique id (any string)
    - started timestamp
    - Environment info
    - Tracked in Redis HSET `processors`

- Completed tasks log
    - E.g. completed HTTP requests
    - Tracked in Redis LIST `past_tasks`

- Task updates pubsub
    - E.g. updated on HTTP requests (start/end)
    - Tracked in Redis PUBSUB `task_updates`

Web tasks
---------

See :py:class:`top.web.task.HTTPTask`.

For the web top, a task presents on HTTP request.

It contains

- HTTP method (`GET`, `POST`)
- Path
- HTTP headers
    - User agent
    - Client IP
- Params (HTTP GET)

Wire protocol example
---------------------

Below is a sample of one JSON record stored in Redis tracker backend

.. code-block:: json

    {
      "process_id": 2125131,
      "thread_id": 140539531953920,
      "process_internal_id": null,
      "task_id": 140538974609616,
      "processor_name": "<Worker 2125131>",
      "started_at": "2022-08-23T15:49:10.905607+00:00",
      "updated_at": "2022-08-23T15:49:11.631117+00:00",
      "ended_at": "2022-08-23T15:49:11.631117+00:00",
      "recorded_successfully": true,
      "tags": null,
      "method": "GET",
      "path": "/api/candles",
      "params": null,
      "uri": null,
      "client_ip_address": "127.0.0.1",
      "request_headers": [
        [
          "HOST",
          "tradingstrategy.ai"
        ],
        [
          "USER-AGENT",
          "python-requests/2.27.1"
        ],
        [
          "ACCEPT",
          "*/*"
        ],
        [
          "ACCEPT-ENCODING",
          "gzip"
        ],
        [
          "CDN-LOOP",
          "cloudflare"
        ],
        [
          "CF-CONNECTING-IP",
          "xx"
        ],
        [
          "CF-IPCOUNTRY",
          "US"
        ],
        [
          "CF-RAY",
          "73f4ff26be5e8226-IAD"
        ],
        [
          "CF-VISITOR",
          "{\"scheme\":\"https\"}"
        ],
        [
          "CONTENT-TYPE",
          "application/json"
        ],
        [
          "X-FORWARDED-FOR",
          "xx, yy"
        ],
        [
          "X-FORWARDED-PROTO",
          "https"
        ]
      ],
      "status_code": 200,
      "status_message": "200 OK",
      "response_headers": [
        [
          "Content-Type",
          "application/json"
        ],
        [
          "Content-Length",
          "429000"
        ],
        [
          "Access-Control-Allow-Origin",
          "*"
        ],
        [
          "Access-Control-Allow-Methods",
          "POST,GET,DELETE,PUT,OPTIONS"
        ],
        [
          "Access-Control-Allow-Headers",
          "Origin, Content-Type, Accept, Authorization"
        ],
        [
          "Access-Control-Allow-Credentials",
          "true"
        ],
        [
          "Access-Control-Max-Age",
          "1728000"
        ]
      ]
    }
