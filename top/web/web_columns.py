"""Column configuration for HTTP tasks."""
from typing import List, Optional

from top.web.colour import map_duration_colour, map_status_code_colour
from top.web.task import HTTPTask

from top.tui.column import TaskColumn


#: Human-readable -> HTTPTask dataclass field/accessor function mappings
#: Records are (accessor function/dataclass field, column width, dynamic function)
# http_task_column_mappings = {
#     "Method": ("method", 6),
#     "Path": ("path", 20),
#     "Worker": ("processor_name", 16),
#     "Duration": ("get_duration", 7),
#     "Ago": ("get_ago", 7),
#     "Resp": ("status_code", 3),
#     "IP": ("client_ip_address", 8),
#     "Length": ("get_content_length", 10),
#     "User agent": ("get_user_agent", 20),
#     "Cty": ("get_ip_country", 2, dynamic_country_column)
# }


#: Define all columns that may appear in HTTP tasks table
def dynamic_country_column(tasks: List[HTTPTask]) -> Optional[str]:
    """Dynamically enable country column if any of HTTPTasks have geolocation info."""
    if any([t.get_ip_country() for t in tasks]):
        return "Cty"
    return None


http_task_columns = TaskColumn.create_map([
    TaskColumn("Method", "method", 6),
    TaskColumn("Path", "path", 20),
    TaskColumn("Worker", "processor_name", 16),
    TaskColumn("Duration", "get_duration", 7, colour_function=map_duration_colour),
    TaskColumn("Ago", "get_ago", 7),
    TaskColumn("Resp", "status_code", 3, colour_function=map_status_code_colour),
    TaskColumn("IP", "client_ip_address", 3),
    TaskColumn("Length", "get_content_length", 10),
    TaskColumn("User agent", "get_user_agent", 20),
    TaskColumn("Cty", "get_ip_country", 2, dynamic_enable_function=dynamic_country_column),
])


default_active_columns = [
    "Cty",
    "Worker",
    "Method",
    "Path",
    "IP",
    "Duration",
    "User agent"
]

default_completed_columns = [
    "Cty",
    "Ago",
    "Resp",
    "Method",
    "Path",
    "Length",
    "User agent"
]

default_recent_columns = [
    "Cty",
    "Ago",
    "Resp",
    "Method",
    "Path",
    "Length",
    "IP",
    "Duration",
    "User agent"
]
