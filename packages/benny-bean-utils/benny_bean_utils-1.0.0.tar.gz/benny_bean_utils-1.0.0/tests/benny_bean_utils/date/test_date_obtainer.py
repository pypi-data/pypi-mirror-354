from datetime import datetime, timedelta
from benny_bean_utils.date.date_obtainer import DateObtainer


class TestDateObtainer:
    def test_today_date(self):
        today = DateObtainer.today_date()
        assert isinstance(today, datetime)
        assert today.date() == datetime.now().date()

    def test_yesterday_date(self):
        yesterday = DateObtainer.yesterday_date()
        assert isinstance(yesterday, datetime)
        assert yesterday.date() == (datetime.now().date() - timedelta(days=1))

    def test_current_week_day(self):
        week_day = DateObtainer.current_week_day()
        assert isinstance(week_day, int)
        assert 0 <= week_day <= 6

    def test_week_number(self):
        week_number = DateObtainer.week_number()
        assert isinstance(week_number, int)
        assert 1 <= week_number <= 53

    def test_remaining_days_before_next_week(self):
        remaining_days = DateObtainer.remaining_days_before_next_week()
        assert isinstance(remaining_days, int)
        assert 0 <= remaining_days <= 6

        today = datetime.now()
        next_week_start = today + timedelta(days=(7 - today.weekday()))
        expected_remaining_days = (next_week_start - today).days
        assert remaining_days == expected_remaining_days