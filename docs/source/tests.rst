Tests
=====

Tests and demos use Redi database #15 through a Docker container.

To run tests

.. code-block:: shell

    # Start redis at localhost:7777
    docker-compose up -d redis
    pytest

Accessing redis
---------------

You can start `redis-cli` with:

.. code-block:: shell

    docker-compose exec redis redis-cli -n 15

View the keys:

.. code-block::

    keys *

Clearing the database:

.. code-block::

    flushdb