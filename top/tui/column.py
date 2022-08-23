"""Column formatting."""
from dataclasses import dataclass
from typing import List, Callable, Any, Protocol, Optional, Dict

from rich.table import Column

from top.core.task import Task


class ColumnColourFunction(Protocol):
    """Define a colour for an individual cell value by a function."""

    def __call__(self, task: Task, value: Any) -> str:
        """Get a row colour for a task.

        See `Rich colour names <https://rich.readthedocs.io/en/stable/appendix/colors.html#appendix-colors>`__.

        :return:
            One of colour names
        """


@dataclass
class TaskColumn:
    """Column definition for task tables.

    Describe how columns will look in the tak table.
    """

    #: Human readable name
    name: str

    #: How to fill the value for this column based on the task.
    #:
    #: Extracts column value from :py:class:`Task` instance.
    #: Dataclass field or accessor function name
    accessor: str

    #: Is this column fixed with
    width: Optional[int] = None

    #: A function to checl if this column is enabled or not
    #:
    #: Gets all table tasks as a parameter and
    #: checks if any of them warrants enabling this column.
    dynamic_enable_function: Optional[Callable] = None

    #: Does this cell value special colours?
    colour_function: Optional[ColumnColourFunction] = None

    @staticmethod
    def create_map(columns: List["TaskColumn"]) -> Dict[str, "TaskColumn"]:
        """Convert list representation to column name -> column map."""
        return {c.name: c for c in columns}


def create_rich_column(column: str, column_mappings: dict) -> Column:
    """Create Rich columns based on column width data."""

    desc = column_mappings[column]
    width = desc.width
    return Column(column, width=width)


def determine_enabled_columns(
        columns: List[str],
        column_mappings: Dict[str, TaskColumn],
        tasks: List[Task]) -> List[str]:
    """Filter visible columns based on the contents of the table.

    E.g. country column is visible only if one of the
    HTTP requests carries geolocation information.

    :param columns:
        List of human-readable column names

    :param column_mappings:
        Mappings of human name -> column desc

    :param tasks:
        List of tasks the dynamic condition is checked against

    :return:
        List of filtered columns
    """
    enabled = []
    for c in columns:
        definition = column_mappings[c]

        dynamic_func = definition.dynamic_enable_function
        if dynamic_func:
            result = dynamic_func(tasks)
            if result:
                enabled.append(result)
        else:
            enabled.append(c)

    return enabled


