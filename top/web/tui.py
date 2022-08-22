"""Text user interface for top-like UI for HTTP requests.

- See `Rich demo <https://github.com/Textualize/rich/blob/master/examples/top_lite_simulator.py>`_ for inspiration.

- See `Arbitrage tracker UI <https://github.com/tradingstrategy-ai/arbitrage-opportunity-tracker/blob/master/order_book_recorder/main.py#L107>`_

"""
import datetime
import time
from dataclasses import fields
from typing import Optional, List

import pkg_resources
import typer

from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.table import Table

from top.integration import get_tracker_by_url_config
from top.redis.tracker import RedisTracker
from top.web.task import HTTPTask

tracker: Optional[RedisTracker] = None

#: Human-readable -> HTTPTask mappings
column_mappings = {
    "Method": "method",
    "Path": "path",
    "Worker": "get_processor_tracking_id",
    "Duration": "get_duration",
    "Ago": "get_ago",
    "Resp": "status_code",
    "IP": "client_ip_address",
    "Length": "get_content_length"
}

default_active_columns = [
    "Worker",
    "Method",
    "Path",
    "IP",
    "Duration"
]

default_completed_columns = [
    "Ago",
    "Resp",
    "Method",
    "Path",
    "Length",
]


def prepare_row(task: HTTPTask, columns: List[str]):
    """Render HTTPTask as a table row by the selected columns.

    Get HTTPTask value either by accessor method or direct attribute.
    """

    # TODO: Build a better framework in the future
    dataclass_fields = {f.name for f in fields(HTTPTask)}

    result = []
    for c in columns:
        key = column_mappings[c]

        if key in dataclass_fields:
            val = getattr(task, key)
        else:
            attr = getattr(task, key)
            val = attr()

        if val:
            if isinstance(val, datetime.timedelta):
                val = f"{val.total_seconds():.2f}"
            elif type(val) == int:
                val = f"{val:,}"
            else:
                val = str(val)
        else:
            val = ""
        result.append(val)
    return result


def fill_tasks_table(
        table: Table,
        tasks: List[HTTPTask],
        columns: List[str],
        max_rows: int):

    tasks.sort(key=lambda t: t.get_processor_tracking_id())

    tasks = tasks[0:max_rows]

    for task in tasks:
        values = prepare_row(task, columns)
        table.add_row(*values)


def create_ui(
    active_columns: List[str],
    completed_columns: List[str],
    width: int,
    height: int) -> Layout:
    """web-top UI using Rich."""

    active_tasks: List[HTTPTask] = list(tracker.get_active_tasks().values())
    completed_tasks: List[HTTPTask] = tracker.get_completed_tasks()

    active = Table(*active_columns,
                   title=f"Active HTTP requests ({len(active_tasks)})",
                   width=width,
                   )

    past = Table(*completed_columns,
                   title=f"Completed HTTP responses ({len(completed_tasks)})",
                 width=width,
                 )

    layout = Layout()
    layout.split_column(
        Layout(name="top"),
        Layout(name="bottom"),
    )

    layout["top"].update(active)
    layout["bottom"].update(past)

    # Show longest duration tasks first
    # active_tasks.sort(key=lambda t: t.get_duration(), reverse=True)

    fill_tasks_table(active, active_tasks, active_columns, height // 2 - 5)
    fill_tasks_table(past, completed_tasks, completed_columns, height // 2 - 5)

    return layout


def version_callback(value: bool):
    """Print out application version.

    See https://typer.tiangolo.com/tutorial/options/version/
    """
    if value:
        my_version = pkg_resources.get_distribution('top-framework').version
        print(f"{my_version}")
        raise typer.Exit()


def main(
    tracker_url: str = typer.Option(..., envvar="TOP_TRACKER_URL", help="Redis database for HTTP request tracking"),
    refresh_rate: float = typer.Option(2.0, envvar="REFRESH_RATE", help="How many seconds have between refreshes"),
    active_columns: str = typer.Option(",".join(default_active_columns), envvar="ACTIVE_COLUMNS", help="Comma separated list of columns to be displayed for active HTTP requests"),
    completed_columns: str = typer.Option(",".join(default_completed_columns), envvar="COMPLETED_COLUMNS", help="Comma separated list of columns to be displayed for completed HTTP requests"),
    version: Optional[bool] = typer.Option(None, help="Show version and exit", callback=version_callback),
):
    """
    web-top shows active and completed request of your web server

    For more information see https://github.com/tradingstrategy-ai/top-framework
    """
    global tracker

    tracker = get_tracker_by_url_config(HTTPTask, tracker_url)

    console = Console()

    active_columns = [c.strip() for c in active_columns.split(",")]
    completed_columns = [c.strip() for c in completed_columns.split(",")]

    with Live(console=console, screen=True, auto_refresh=False) as live:
        while True:
            ui = create_ui(active_columns, completed_columns, console.size.width, console.size.height)
            live.update(ui, refresh=True)
            time.sleep(refresh_rate)


def start():
    """Poetry entrypoint."""
    typer.run(main)


if __name__ == "__main__":
    typer.run(main)
