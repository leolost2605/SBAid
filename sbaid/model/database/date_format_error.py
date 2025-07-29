"""This module contains the DateFormatError class."""


class DateFormatError(Exception):
    """This exception is raised when a date format is not supported."""
    def __init__(self, message: str) -> None:
        super().__init__(message)
