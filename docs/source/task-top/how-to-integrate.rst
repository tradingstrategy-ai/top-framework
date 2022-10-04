How to integrate your Python application
=======================================

- You need a backend for the active task tracking.
  The default suggested backend is :ref:`Redis`.

- You need to configure the tracking for `task-top`

- You need to decorate your tasks with :py:func:`top.longrunning.decorator.track`

Then you can use it like this:

.. include:: ../../../scripts/long-running-example.py