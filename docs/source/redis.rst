.. _redis:

Redis tracking backend
======================

Redis tracking backend stores active and completed requests in Redis

Benefits
--------

- Minimal modifications needed to your application or web server

- Easy to set up

How does it work
----------------

For each task/request we make start end end write in Redis.

See :py:class:`top.redis.tracker.Tracker` class for example.

- You can use the class as-is from any Python application

- Creating your own task update logic in other programming languages is straightforward

More information
----------------

See :ref:`data structure`.