"""HTTP task colouring."""
from top.web.task import HTTPTask


def colour_by_status(t: HTTPTask):
    """Set row colour by its HTTP status.

    `See the colour map <https://rich.readthedocs.io/en/stable/appendix/colors.html#appendix-colors>`_.
    """

    if not t.status_code:
        # Still active
        return "white"
    elif t.status_code < 300:
        # 200-299 good
        return "green"
    elif t.status_code < 400:
        # 300-399 redirect
        return "yellow"
    elif t.status_code < 500:
        # 400-499 redirect
        return "red"
    elif t.status_code >= 500 and t.status_code < 600:
        # 500+ bad
        return "red"
    else:
        # No idea?
        return "bright_magenta"


def colour_by_duration(t: HTTPTask):
    """Set row colour by its duration.

    `See the colour map <https://rich.readthedocs.io/en/stable/appendix/colors.html#appendix-colors>`_.
    """

    duration = t.get_duration().total_seconds()
    if duration < 1.0:
        return "green"
    elif duration < 2.5:
        return "yellow"
    else:
        return "red"
