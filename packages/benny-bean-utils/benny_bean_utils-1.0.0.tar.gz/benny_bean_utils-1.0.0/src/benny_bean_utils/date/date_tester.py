from datetime import datetime


class DateTester:
    """
    A class to test date-related functionalities.
    """

    @staticmethod
    def is_date_in_less_than_x_days(date: datetime, days: int) -> bool:
        """
        Checks if the given date is within the next 'days' days from today.

        :param date: The date to check.
        :param days: The number of days to check against.
        :return: True if the date is within the next 'days' days, False otherwise.
        """
        today = datetime.now().date()
        target = date.date()
        return 0 <= (target - today).days <= days

    @staticmethod
    def is_today(date: datetime) -> bool:
        """
        Checks if the given date is today.

        :param date: The date to check.
        :return: True if the date is today, False otherwise.
        """
        return date.date() == datetime.now().date()