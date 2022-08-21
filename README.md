A generic Python framework for writing UNIX top like Text User Interface applications.

It comes with an example `web-top` application to give `top` like monitoring tool
for HTTP requests on any web server.

# Use cases

- HTTP request trackers for web servers
- Active task trackers for Cron/Celery/other background job managers

The core concepts of the framework are *processors*, usually OS processes/threads
that are currently handling active *tasks*. Depending on the context a task 
can be a HTTP request, a UNIX process, or something else.

# Dependencies

- Python 3.9+
- Redis: Used to track started/ended tasks

The task tracking backend is abstract: If you do not want to use Redis you can replace
with your own solution as the interface is only few lines of Python.

# Overview

The *Top Framework* consists of few parts

- *Tracker backend*: to track and store tasks are currently active and completed 
- *Client library*: to emit events when a task starts and ends
- *Text user interface*: A command line application that gives you a nice `top` view over your tasks

# Design goals

See documentation

# Data structures

See documentation

