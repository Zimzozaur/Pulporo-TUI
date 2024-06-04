from datetime import datetime


def format_date_string(date_string: str) -> str:
    """Formats a date string to YYYY-MM-DD HH:MM:SS format.

    Args:
      date_string: The date string in ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ).

    Returns:
      The formatted date string (YYYY-MM-DD HH:MM:SS).
    """
    return datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M:%S")

