import re
from datetime import datetime

from textual.validation import Validator, ValidationResult


class TitleMax50Validator(Validator):
    def validate(self, value: str) -> ValidationResult:
        if len(value) > 50:
            return self.failure('Title cannot be longer than 50 chars')
        if len(value) < 1:
            return self.failure('Title cannot be an empty string')
        return self.success()


class DateValidator(Validator):
    def validate(self, value: str) -> ValidationResult:
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', value):
            return self.failure("Input must be a date in the format year-month-day (e.g., 2024-05-31)")
        try:
            datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            return self.failure("Invalid date")
        return self.success()


