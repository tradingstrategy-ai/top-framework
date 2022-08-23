Demo
----

To demo `web-top`

Set up Redis (use docker).

Set up :doc:`Gunicorn <./gunicorn>`.

Launch the traffic generator:

.. code-block:: shell

    poetry run random-http-requests

Launch `web-top`:

.. code-block:: shell

    poetry run web-top live
