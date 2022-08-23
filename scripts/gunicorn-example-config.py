"""Example configuration file for Gunicorn.

Server hooks can be set only through config file, not command line.
"""
import top.gunicorn.hooks

when_ready = top.gunicorn.hooks.when_ready
pre_request = top.gunicorn.hooks.pre_request
post_request = top.gunicorn.hooks.post_request
