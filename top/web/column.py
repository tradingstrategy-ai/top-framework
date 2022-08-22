"""Column configuration for HTTP tasks."""

#: Human-readable -> HTTPTask dataclass field/accessor function mappings
http_task_column_mappings = {
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
