"""This module contains the ForeignKeyError class."""


class ForeignKeyError(Exception):
    """Exception raised when a foreign key error is encountered."""
    def __init__(self, message: str) -> None:
        super().__init__(message)
