"""Dynamic country column."""
from typing import List, Optional

from top.web.task import HTTPTask


def dynamic_country_column(tasks: List[HTTPTask]) -> Optional[str]:
    """Dynamically enable country column if any of requests have geolocation info."""

    if any([t.get_ip_country() for t in tasks]):
        return "Cty"
    return None