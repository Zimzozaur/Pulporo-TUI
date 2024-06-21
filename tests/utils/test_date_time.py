from utils import format_date_string


def test_string_with_microseconds():
    result = format_date_string('2024-06-20T12:30:45Z')
    assert result == '2024-06-20 12:30:45'


def test_string_without_microseconds():
    result = format_date_string('2024-06-20T12:30:45.123456Z')
    assert result == '2024-06-20 12:30:45'


