from typing import List

from rich.table import Column


def create_column(column: str, column_mappings: dict) -> Column:
    """Create Rich columns based on column width data."""

    desc = column_mappings[column]
    width = desc[1]
    return Column(column, width=width)
