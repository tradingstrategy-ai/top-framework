"""Column definitions for HTTP tasks."""

from typing import List, Optional

from top.web.colour import map_duration_colour, map_status_code_colour
from top.web.task import HTTPTask

from top.tui.column import TaskColumn


#: Define all columns that may appear in HTTP tasks table
def dynamic_country_column(tasks: List[HTTPTask]) -> Optional[str]:
    """Dynamically enable country column if any of HTTPTasks have geolocation info."""
    if any([t.get_ip_country() for t in tasks]):
        return "Cty"
    return None


http_task_columns = TaskColumn.create_map(
    [
        TaskColumn("Cty", "get_ip_country", 2, dynamic_enable_function=dynamic_country_column),
        TaskColumn("IP", "get_original_ip", 16),
        TaskColumn("Method", "method", 6),
        TaskColumn("Path", "path", 20),
        TaskColumn("Worker", "processor_name", 16),
        TaskColumn("Duration", "get_duration", 7, colour_function=map_duration_colour),
        TaskColumn("Ago", "get_ago", 7),
        TaskColumn("Resp", "status_code", 3, colour_function=map_status_code_colour),
        TaskColumn("Length", "get_content_length", 10),
        TaskColumn("User agent", "get_user_agent", max_width=20),
    ]
)


default_active_columns = ["Cty", "IP", "Worker", "Method", "Path", "Duration", "User agent"]

default_completed_columns = ["Cty", "IP", "Ago", "Duration", "Resp", "Method", "Path", "Length", "User agent"]

default_recent_columns = ["Cty", "IP", "Ago", "Duration", "Resp", "Method", "Path", "Length", "User agent"]
