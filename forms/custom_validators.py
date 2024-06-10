import re
from datetime import datetime

from textual.validation import Validator, ValidationResult


class TitleMax50Validator(Validator):
    def validate(self, value: str) -> ValidationResult:
        """
        Validate the title string.

        Args:
            value (str): The title to be validated.

        Returns:
            ValidationResult: The result of the validation.
                - Returns failure if the title is longer than 50 characters.
                - Returns failure if the title is an empty string.
                - Returns success if the title meets both criteria.
        """
        if len(value) > 50:
            return self.failure('Title cannot be longer than 50 chars')
        if len(value) < 1:
            return self.failure('Title cannot be an empty string')
        return self.success()


class ValueValidator(Validator):
    def validate(self, value: str) -> ValidationResult:
        """
        Validate the value string.

        Args:
            value (str): The value to be validated. It should be a numeric string.

        Returns:
            ValidationResult: The result of the validation.
                - Returns failure if the value does not match the format of an integer or a float
                  with exactly two decimal places. For example, valid formats are '123' or '123.45'.
                  Invalid formats include '123.4', '123.456', and 'abc'.
                - Returns success if the value meets the criteria.
        """
        if not re.match(r'^\d+(\.\d{2})?$', value):
            return self.failure('Number has to have 2 digits after decimal point')
        return self.success()


class DateValidator(Validator):
    def validate(self, value: str) -> ValidationResult:
        """
        Validate the date string.

        Args:
            value (str): The date to be validated. It should be in the format 'YYYY-MM-DD'.

        Returns:
            ValidationResult: The result of the validation.
                - Returns failure if the date is not in the format 'YYYY-MM-DD'. (e.g., '2024-03-7')
                - Returns failure if the date is invalid (e.g., '2024-02-30' is not a valid date).
                - Returns success if the date meets both criteria.
        """
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', value):
            return self.failure("Input must be a date in the format year-month-day (e.g., 2024-05-09)")
        try:
            datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            return self.failure("Invalid date")
        return self.success()

