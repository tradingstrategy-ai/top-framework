"""Column configuration for HTTP tasks."""


from top.web.country_column import dynamic_country_column

#: Human-readable -> HTTPTask dataclass field/accessor function mappings
#: Records are (accessor function/dataclass field, column width, dynamic function)
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
    "Cty": ("get_ip_country", 2, dynamic_country_column)
}

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
