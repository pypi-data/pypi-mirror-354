from datetime import datetime

from benny_bean_utils.date.date_formatter import DateFormatter, DEFAULT_DATE_FORMAT

class TestDateFormatter:
    def test__init__(self):
        date_formatter = DateFormatter()
        assert date_formatter._date_format == DEFAULT_DATE_FORMAT
        date_formatter = DateFormatter("%Y-%m-%d")
        assert date_formatter._date_format == "%Y-%m-%d"

    def test_format_date(self):
        date_formatter = DateFormatter("%Y-%m-%d")
        date = datetime(2023, 10, 1)
        formatted_date = date_formatter.format_date(date)
        assert formatted_date == "2023-10-01"

    def test_parse_date(self):
        date_formatter = DateFormatter("%Y-%m-%d")
        date_str = "2023-10-01"
        parsed_date = date_formatter.parse_date(date_str)
        assert parsed_date == datetime(2023, 10, 1)