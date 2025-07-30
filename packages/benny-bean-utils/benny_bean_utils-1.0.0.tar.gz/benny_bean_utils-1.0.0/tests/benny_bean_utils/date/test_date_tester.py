from datetime import datetime, timedelta
from benny_bean_utils.date import DateTester

class TestDateTester:
    def test_is_date_in_less_than_x_days(self):
        from datetime import timedelta


        # Test with a date in the future
        future_date = datetime.now() + timedelta(days=5)
        assert DateTester.is_date_in_less_than_x_days(future_date, 7) is True

        # Test with a date beyond the specified days
        distant_future_date = datetime.now() + timedelta(days=10)
        assert DateTester.is_date_in_less_than_x_days(distant_future_date, 7) is False

        # Test with today's date
        today_date = datetime.now()
        assert DateTester.is_date_in_less_than_x_days(today_date, 1) is True

        # Test with a date in the past
        past_date = datetime.now() - timedelta(days=1)
        assert DateTester.is_date_in_less_than_x_days(past_date, 1) is False

    def test_is_today(self):

        # Test with today's date
        today_date = datetime.now()
        assert DateTester.is_today(today_date) is True

        # Test with a date in the past
        past_date = datetime.now() - timedelta(days=1)
        assert DateTester.is_today(past_date) is False

        # Test with a date in the future
        future_date = datetime.now() + timedelta(days=1)
        assert DateTester.is_today(future_date) is False