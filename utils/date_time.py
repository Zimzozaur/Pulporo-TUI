from datetime import datetime


def format_date_string(date_string: str) -> str:
    """Formats a date string to YYYY-MM-DD HH:MM:SS format.

    Args:
      date_string: The date string in ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ or YYYY-MM-DDTHH:MM:SS.ssssssZ).

    Returns:
      The formatted date string (YYYY-MM-DD HH:MM:SS).
    """
    # Determine if the date string contains microseconds
    if '.' in date_string:
        # Parse with microseconds
        parsed_date = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
    else:
        # Parse without microseconds
        parsed_date = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")

    # Format the date to the desired format
    return parsed_date.strftime("%Y-%m-%d %H:%M:%S")