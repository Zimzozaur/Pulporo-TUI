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
        if not re.match(r'^\d{1,2}-\d{1,2}-\d{4}$', value):
            return self.failure("Input must be a date in the format day-month-year (e.g., 1-1-2024)")
        try:
            datetime.strptime(value, '%d-%m-%Y')
        except ValueError:
            return self.failure("Invalid date")
        return self.success()


