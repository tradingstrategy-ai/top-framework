"""Column configuration for HTTP tasks."""

#: Human-readable -> HTTPTask dataclass field/accessor function mappings
http_task_column_mappings = {
    "Method": ("method", 6),
    "Path": ("path", 20),
    "Worker": ("processor_name", 16),
    "Duration": ("get_duration", 7),
    "Ago": ("get_ago", 7),
    "Resp": ("status_code", 3),
    "IP": ("client_ip_address", 8),
    "Length": ("get_content_length", 10),
    "User agent": ("get_user_agent", 20),
}

default_active_columns = [
    "Worker",
    "Method",
    "Path",
    "IP",
    "Duration",
    "User agent"
]

default_completed_columns = [
    "Ago",
    "Resp",
    "Method",
    "Path",
    "Length",
    "User agent"
]

default_recent_columns = [
    "Ago",
    "Resp",
    "Method",
    "Path",
    "Length",
    "IP",
    "Duration",
    "User agent"
]
