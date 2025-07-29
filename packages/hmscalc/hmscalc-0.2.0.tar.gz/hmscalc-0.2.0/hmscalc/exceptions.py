"""Custom exception classes for HMS time calculations."""


class HMSTimeError(Exception):
    """Base exception for HMS time errors."""

    pass


class InvalidTimeFormatError(HMSTimeError):
    """Exception raised for invalid time format strings."""

    def __init__(self, time_str: str):
        """Initialize with the invalid time string."""
        super().__init__(f"Invalid time format: '{time_str}'")


class NotTimeStringError(HMSTimeError):
    """Exception raised when a non-string is provided as a time input."""

    def __init__(self, value):  # type: ignore[no-untyped-def]
        """Initialize with the invalid value type."""
        super().__init__(f"Time input must be a string, got: {type(value).__name__}")
