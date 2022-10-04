Development
===========

Checkout from Github.

Then:

.. code-block:: shell

    poetry shell
    poetry install -E gunicorn -E docs

To start Redis for tests:

.. code-block:: shell

    docker-compose up -d redis

Run tests:

.. code-block:: shell

    pytest

Formatting code
---------------


