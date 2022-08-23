"""HTTP task colouring.

`See the colour map <https://rich.readthedocs.io/en/stable/appendix/colors.html#appendix-colors>`_.
"""
import datetime
from typing import Optional

from top.web.task import HTTPTask


def colour_row_by_status(t: HTTPTask):
    """Set row colour by its HTTP status.

    """
    return map_status_code_colour(t, t.status_code)


def colour_row_by_duration(t: HTTPTask):
    """Set row colour by its duration.

    """

    duration = t.get_duration().total_seconds()
    return map_duration_colour(t, duration)


def map_duration_colour(task: HTTPTask, duration: Optional[datetime.timedelta]):
    """Get row/value colour for request duration."""

    if not duration:
        return "white"

    s = duration.total_seconds()

    if s < 1.0:
        return "green"
    elif s < 2.5:
        return "yellow"
    else:
        return "red"


def map_status_code_colour(t: HTTPTask, status_code: Optional[int]):
    """Set row colour by its HTTP status.

    """

    if not status_code:
        # Still active
        return "white"
    elif status_code < 300:
        # 200-299 good
        return "green"
    elif status_code < 400:
        # 300-399 redirect
        return "yellow"
    elif status_code < 500:
        # 400-499 redirect
        return "red"
    elif status_code >= 500 and status_code < 600:
        # 500+ bad
        return "red"
    else:
        # No idea?
        return "bright_magenta"


