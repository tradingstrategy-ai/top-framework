import datetime

from dataclasses import fields
from typing import List, Optional, Protocol, Dict

from rich.table import Table, Text

from top.core.task import Task
from top.tui.column import TaskColumn


class RowColourFunction(Protocol):
    """Define row colour by a function."""

    def __call__(self, task: Task) -> str:
        """Get a row colour for a task.

        See `Rich colour names <https://rich.readthedocs.io/en/stable/appendix/colors.html#appendix-colors>`__.

        :return:
            One of colour names
        """


def prepare_row(
    task: Task,
    columns: List[str],
    column_mappings: Dict[str, TaskColumn],
) -> List[str]:
    """Render Task as a table row by the selected columns.

    Get HTTPTask value either by accessor method or direct attribute.

    :param columns:
        List of human-readable column names to appear in this row

    :param column_mappings:
        Task attribute to human-readable column mappings

    :return:
        Table row values as list
    """

    # TODO: Build a better framework in the future
    dataclass_fields = {f.name for f in fields(task.__class__)}

    result = []
    for c in columns:

        definition = column_mappings[c]
        key = definition.accessor

        if key in dataclass_fields:
            raw_val = getattr(task, key)
        else:
            attr = getattr(task, key)

            try:
                raw_val = attr()
            except Exception as e:
                raise ValueError(f"Could not call accessor function {attr} for task {task}") from e

        # Convert value object to string
        if raw_val:
            if isinstance(raw_val, datetime.timedelta):
                val = f"{raw_val.total_seconds():.2f}"
            elif type(raw_val) == int:
                val = f"{raw_val:,}"
            else:
                val = str(raw_val)
        else:
            val = ""

        if definition.colour_function:
            t = Text(val)
            colour = definition.colour_function(task, raw_val)
            t.stylize(colour)
            val = t

        result.append(val)

    return result


def fill_tasks_table(
    table: Table,
    tasks: List[Task],
    columns: List[str],
    column_mappings: dict,
    max_rows: Optional[int] = None,
    colour_function: Optional[RowColourFunction] = None,
):
    """Fill a Rich table with tasks as rows.

    Tasks are added as rows to the table, from top to bottom.

    :param table:
        Rich table we render into

    :param tasks:
        List of tasks to render

    :param columns:
        List of human-readable column nams

    :param column_mappings:
        Task attribute to human-readable column mappings

    :param colour_function:
        A function to decide row colour based on task

    :param max_rows:
        How many rows we can fit on the console screen before overflow
    """

    if max_rows:
        tasks = tasks[0:max_rows]

    for task in tasks:
        values = prepare_row(task, columns, column_mappings)
        table.add_row(*values)

    if colour_function:
        row_styles = [colour_function(t) for t in tasks]
        table.row_styles = row_styles
