"""Text user interface for top-like UI for HTTP requests.

The entry point to the application is configured in `pyproject.toml`.
"""
import enum
import time
from typing import List, Optional

import pkg_resources
import typer

from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.table import Table

from top.integration import get_tracker_by_url_config
from top.redis.tracker import RedisTracker
from top.tui.column import create_rich_column, determine_enabled_columns
from top.tui.row import fill_tasks_table
from top.web.colour import colour_row_by_status
from top.web.web_columns import default_active_columns, default_completed_columns, http_task_columns, \
    default_recent_columns
from top.web.task import HTTPTask

help_text = """
web-top is an interactive HTTP request monitor.

For more information see https://github.com/tradingstrategy-ai/top-framework
"""

app = typer.Typer(help=help_text)


class RecentMode(enum.Enum):
    """What do we print out in recent requests print out."""
    all = "all"
    active = "active"
    complete = "complete"


def create_ui(
        tracker: RedisTracker,
        active_columns: List[str],
        completed_columns: List[str],
        column_mappings: dict,
        width: int,
        height: int) -> Layout:
    """web-top UI using Rich."""

    active_tasks: List[HTTPTask] = list(tracker.get_active_tasks().values())
    completed_tasks: List[HTTPTask] = tracker.get_completed_tasks()

    active_columns = determine_enabled_columns(active_columns, column_mappings, active_tasks)
    completed_columns = determine_enabled_columns(completed_columns, column_mappings, completed_tasks)

    active = Table(*[create_rich_column(c, column_mappings) for c in active_columns],
                   title=f"Active HTTP requests ({len(active_tasks)})",
                   width=width,
                   border_style="bright_black",
                   )

    past = Table(*[create_rich_column(c, column_mappings) for c in completed_columns],
                 title=f"Completed HTTP responses ({len(completed_tasks)})",
                 width=width,
                 border_style="bright_black",
                 )

    layout = Layout()
    layout.split_column(
        Layout(name="top"),
        Layout(name="bottom"),
    )

    layout["top"].update(active)
    layout["bottom"].update(past)

    # Show the longest duration tasks first
    active_tasks.sort(key=lambda t: t.get_duration(), reverse=True)

    # Decoration takes 5 rows per table
    rows_height = height - 10

    fill_tasks_table(
        active,
        active_tasks,
        active_columns,
        column_mappings,
        rows_height // 2,
        None)

    fill_tasks_table(
        past,
        completed_tasks,
        completed_columns,
        column_mappings,
        rows_height // 2,
        None)

    return layout


@app.command()
def version():
    """Print out application version.

    See https://typer.tiangolo.com/tutorial/options/version/
    """
    my_version = pkg_resources.get_distribution('top-framework').version
    print(f"{my_version}")


@app.command()
def live(
        tracker_url: str = typer.Option(..., envvar="TOP_TRACKER_URL", help="Redis database for HTTP request tracking"),
        refresh_rate: float = typer.Option(2.0, envvar="TOP_REFRESH_RATE",
                                           help="How many seconds have between refreshes"),
        active_columns: str = typer.Option(", ".join(default_active_columns), envvar="ACTIVE_COLUMNS",
                                           help="Comma separated list of columns to be displayed for active HTTP requests"),
        completed_columns: str = typer.Option(", ".join(default_completed_columns), envvar="COMPLETED_COLUMNS",
                                              help="Comma separated list of columns to be displayed for completed HTTP requests"),
):
    """
    Interactive monitor for active and completed request of your web server.
    """

    tracker = get_tracker_by_url_config(HTTPTask, tracker_url)

    console = Console()

    active_columns = [c.strip() for c in active_columns.split(",")]
    completed_columns = [c.strip() for c in completed_columns.split(",")]

    with Live(console=console, screen=True, auto_refresh=False) as live:
        while True:
            ui = create_ui(
                tracker,
                active_columns,
                completed_columns,
                http_task_columns,
                console.size.width,
                console.size.height)
            live.update(ui, refresh=True)
            time.sleep(refresh_rate)


@app.command()
def recent(
        tracker_url: str = typer.Option(..., envvar="TOP_TRACKER_URL", help="Redis database for HTTP request tracking"),
        columns: str = typer.Option(", ".join(default_recent_columns), envvar="TOP_RECENT_COLUMNS",
                                    help="Comma separated list of columns to be displayed for HTTP requests"),
        mode: RecentMode = typer.Option("all", envvar="TOP_RECENT_MODE",
                                        help="Do we print all, active or complete requests"),
        limit: Optional[int] = typer.Option(None, envvar="TOP_RECENT_LIMIT", help="How many rows to print (max)"),
):
    """
    Print out HTTP requests.

    Print out currently active and recent
    """

    tracker = get_tracker_by_url_config(HTTPTask, tracker_url)
    columns = [c.strip() for c in columns.split(",")]

    active_tasks: List[HTTPTask] = list(tracker.get_active_tasks().values())
    completed_tasks: List[HTTPTask] = tracker.get_completed_tasks()

    # Show the longest duration first
    active_tasks.sort(key=lambda t: t.get_duration(), reverse=True)

    if mode == RecentMode.active:
        tasks = active_tasks
    elif mode == RecentMode.complete:
        tasks = completed_tasks
    else:
        tasks = active_tasks + completed_tasks

    columns = determine_enabled_columns(columns, http_task_columns, tasks)

    table = Table(*columns, title=f"HTTP requests ({len(tasks)})")

    fill_tasks_table(
        table,
        tasks,
        columns,
        http_task_columns,
        limit,
        colour_row_by_status,
    )

    console = Console()
    console.print(table)


if __name__ == "__main__":
    # Execute typer entry point
    app()
