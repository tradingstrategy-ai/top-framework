Data structure
==============

Preface
-------

All data is serialised as JSON and readable to any application,
any programming language, easily.

Task emitters and TUI communicate over a a tracker backend.
The default tracker backend is
Redis, but this is easily replaceable, because the interface
code is only few hundreds of lines of Python.
For OS `top` like process tracker you do not need a backend at all,
because you can get this information directly from your kernel.

Generic tasks and processors structure
--------------------------------------

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

For the web top, a task presents on HTTP request.

It contains

- HTTP method (`GET`, `POST`)
- Path
- HTTP headers
    - User agent
    - Client IP
- Params (HTTP GET)
