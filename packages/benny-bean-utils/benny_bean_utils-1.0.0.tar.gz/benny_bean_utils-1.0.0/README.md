# Benny Bean Utils Package

## Description
This package targets to offer basic utilities for my personal projects.

## Installation

### To build the package : 
```bash
py -m pip install --upgrade build
py -m build
```

### To upload the package to PyPI:
```bash
py -m pip install --upgrade twine
py -m twine upload dist/*
```

### To install the package:
```bash
py -m pip install benny_bean_utils
```

## Utilities

### Date Utilities

#### DateFormatter
A class for formatting and parsing dates according to a specified format.

```python
from datetime import datetime
from benny_bean_utils.date.date_formatter import DateFormatter

# Initialize with default format (%d/%m/%Y) or custom format
formatter = DateFormatter()
# or
formatter = DateFormatter("%Y-%m-%d")

# Format a date
date = datetime.now()
formatted_date = formatter.format_date(date)  # "12/06/2025" with default format

# Parse a date string
date_obj = formatter.parse_date("12/06/2025")  # Returns a datetime object
```

#### DateObtainer
A utility class for obtaining various date-related information.

```python
from benny_bean_utils.date.date_obtainer import DateObtainer

# Get today's date
today = DateObtainer.today_date()  # Returns datetime object

# Get yesterday's date
yesterday = DateObtainer.yesterday_date()  # Returns datetime object

# Get current week day (0=Monday, 6=Sunday)
weekday = DateObtainer.current_week_day()  # Returns int (0-6)

# Get current week number
week_num = DateObtainer.week_number()  # Returns int

# Get days remaining before next week
days_to_next_week = DateObtainer.remaining_days_before_next_week()  # Returns int
```

#### DateTester
A class to test date-related functionalities.

```python
from datetime import datetime
from benny_bean_utils.date.date_tester import DateTester

# Check if a date is within X days from today
date = datetime.now()
is_within_days = DateTester.is_date_in_less_than_x_days(date, 5)  # Returns boolean

# Check if a date is today
is_today = DateTester.is_today(date)  # Returns boolean
```

### String Utilities

#### StringFormatter
Utility class for string formatting operations.

```python
from benny_bean_utils.string.string_formatter import StringFormatter

# Convert text to snake_case
snake_case = StringFormatter.get_snake_case_of_text("Hello World")  # Returns "hello_world"
text_with_accents = StringFormatter.get_snake_case_of_text("Café au lait")  # Returns "cafe_au_lait"
```