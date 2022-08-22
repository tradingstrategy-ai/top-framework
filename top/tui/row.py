import datetime
from dataclasses import fields
from typing import List

from rich.table import Table

from top.core.task import Task


def prepare_row(task: Task,
                columns: List[str],
                column_mappings: dict,
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
        key = column_mappings[c]

        if key in dataclass_fields:
            val = getattr(task, key)
        else:
            attr = getattr(task, key)

            try:
                val = attr()
            except Exception as e:
                raise ValueError(f"Could not call accessor function {attr} for task {task}") from e

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
        tasks: List[Task],
        columns: List[str],
        column_mappings: dict,
        max_rows: int):
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

    :param max_rows:
        How many rows we can fit on the console screen before overflow
    """
    tasks = tasks[0:max_rows]

    for task in tasks:
        values = prepare_row(task, columns, column_mappings)
        table.add_row(*values)
