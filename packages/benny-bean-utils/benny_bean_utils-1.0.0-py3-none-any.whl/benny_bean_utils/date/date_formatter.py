from datetime import datetime

DEFAULT_DATE_FORMAT = "%d/%m/%Y"

class DateFormatter:
    """
    A class for formatting and parsing dates according to a specified format.
    """
    _date_format: str

    def __init__(self, date_format: str = DEFAULT_DATE_FORMAT) -> None:
        """
        Initializes the DateFormatter with a specified date format.

        :param date_format: The format to use for formatting dates.
        """
        self._date_format = date_format

    def format_date(self, date: datetime) -> str:
        """
        Formats the given date according to the specified date format.

        :param date: The date to format.
        :return: The formatted date as a string.
        """
        return date.strftime(self._date_format)

    def parse_date(self, date_str: str) -> datetime:
        """
        Parses a date string into a datetime object according to the specified date format.

        :param date_str: The date string to parse.
        :return: The parsed datetime object.
        """
        return datetime.strptime(date_str, self._date_format)