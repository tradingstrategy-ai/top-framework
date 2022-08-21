Tests
=====

To run tests

.. code-block:: shell

    # Start redis at localhost:7777
    docker-compose up -d redis

    export REDIS_PASSWORD="add your password here"
    export TOP_REDIS_URL="redis://:${REDIS_PASSWORD}@localhost:7777/15"

    pytest