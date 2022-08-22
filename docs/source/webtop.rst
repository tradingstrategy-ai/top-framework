web-top
=======

`web-top` is a top-like tool to show active and completed
HTTP requets on your web server.

Supported web servers
--------------------

- `gunicorn <https://docs.gunicorn.org/>`_

Supported tracking backends
---------------------------

- `Redis <https://redis.io/>`_

Using web-top with Gunicorn
---------------------------

To get HTTP request tracking with `web-top`

- You need to install `web-top` Python package in the same Python
  virtual environment as you have Gunicorn

- You need to have a Redis server installed, as it will
  store the status of active and completed requests

Set `web-top` configuration

.. code-block:: shell

    export TOP_TRACKER_URL="redis://localhost:7777/15"

Create a Gunicorn config file where tracking hooks are set.
Example `gunicorn-config-example.py:

.. code-block:: python

    import top.gunicorn.hooks

    when_ready = top.gunicorn.hooks.when_ready
    pre_request = top.gunicorn.hooks.pre_request
    post_request = top.gunicorn.hooks.post_request

Start Gunicorn with the integration hooks:

.. code-block:: shell

    gunicorn \
        --bind=127.0.0.1:8080 \
        --workers=2 \
        --config=top/gunicorn/example_config.py \
        --log-level=debug \
        --access-logfile /dev/stdout \
        "top.gunicorn.testapp:slow_app"

Demo
~~~~

Start Gunicorn as in the above example.

Start load generator:

.. code-block:: python

    poetry run random-http-requests

Start web-top:

.. code-block:: python

    poetry run web-top

