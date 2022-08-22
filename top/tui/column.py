"""Column formatting."""

from typing import List

from rich.table import Column

from top.core.task import Task


def create_column(column: str, column_mappings: dict) -> Column:
    """Create Rich columns based on column width data."""

    desc = column_mappings[column]
    width = desc[1]
    return Column(column, width=width)


def determine_enabled_columns(
        columns: List[str],
        column_mappings: dict,
        tasks: List[Task]) -> List[str]:
    """Filter visible columns based on the contents of the table.

    E.g. country column is visible only if one of the
    HTTP requests carries geolocation information.

    :param columns:
        List of human readable column names

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
        try:
            dynamic_func = definition[2]
            result = dynamic_func(tasks)
            if result:
                enabled.append(result)
        except IndexError:
            enabled.append(c)

    return enabled


