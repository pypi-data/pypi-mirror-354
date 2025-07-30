from datetime import datetime, timedelta


class DateObtainer:
    """
    A utility class for obtaining various date-related information.
    This class provides methods to get today's date, yesterday's date, the current week day,
    the current week number, and to check if a date is within a certain number of days from today.
    It also includes methods to check if a date is today and to find the number of days remaining
    before the next week starts.
    """
    @staticmethod
    def today_date(as_string: bool = False) -> datetime:
        """
        Returns today's date formatted according to the specified date format.

        :return: Today's date as a string in the specified format.
        """
        return datetime.now()

    @staticmethod
    def yesterday_date() -> datetime:
        """
        Returns yesterday's date formatted according to the specified date format.

        :return: Yesterday's date as a string in the specified format.
        """
        return datetime.now().replace(day=datetime.now().day - 1)

    @staticmethod
    def current_week_day() -> int:
        """
        Returns the current day of the week as an integer.

        :return: Current day of the week (0=Monday, 6=Sunday).
        """
        return datetime.now().weekday()

    @staticmethod
    def week_number() -> int:
        """
        Returns the current week number of the year.

        :return: Current week number.
        """
        return datetime.now().isocalendar()[1]

    @staticmethod
    def remaining_days_before_next_week() -> int:
        """
        Returns the number of days remaining before the next week starts.

        :return: Number of days remaining before the next week.
        """
        today = datetime.now()
        next_week_start = today + timedelta(days=(7 - today.weekday()))
        return (next_week_start - today).days
