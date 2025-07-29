"""Module for handling time in hours, minutes, and seconds (HMS) format."""

import re
from typing import Iterable

from .exceptions import InvalidTimeFormatError, NotTimeStringError


class HMSTime:
    """Class to represent and manipulate time in hours, minutes, and seconds (HMS) format.

    Args:
    ----
        time_str (str): Time string to parse.

    """

    def __init__(self, time_str: str):
        """Initialize HMSTime from a time string in 'HH:MM:SS' or 'HH:MM' format.

        Args:
        ----
            time_str (str): Time string to parse.

        """
        self.total_seconds = self._parse_time_string(time_str)

    def __add__(self, other: "HMSTime") -> "HMSTime":
        """Add two HMSTime objects and return a new HMSTime object.

        Args:
        ----
            other (HMSTime): The other HMSTime object to add.

        Returns:
        -------
            HMSTime: The sum of the two times.

        """
        return HMSTime.from_seconds(self.total_seconds + other.total_seconds)

    def __sub__(self, other: "HMSTime") -> "HMSTime":
        """Subtract another HMSTime object from this one and return a new HMSTime object.

        Args:
        ----
            other (HMSTime): The other HMSTime object to subtract.

        Returns:
        -------
            HMSTime: The difference of the two times.

        """
        return HMSTime.from_seconds(self.total_seconds - other.total_seconds)

    def __str__(self) -> str:
        """Return the string representation of the HMSTime object in 'HH:MM:SS' format.

        Returns
        -------
            str: The string representation of the HMSTime object.

        """
        total = abs(self.total_seconds)
        hh = total // 3600
        mm = (total % 3600) // 60
        ss = total % 60
        sign = "-" if self.total_seconds < 0 else ""
        return f"{sign}{hh}:{mm:02}:{ss:02}"

    def __repr__(self) -> str:
        """Return the official string representation of the HMSTime object."""
        return f"HMSTime('{self}')"

    def __eq__(self, other: object) -> bool:
        """Check if two HMSTime objects are equal."""
        if not isinstance(other, HMSTime):
            return NotImplemented
        return self.total_seconds == other.total_seconds

    def __lt__(self, other: "HMSTime") -> bool:
        """Check if this HMSTime object is less than another."""
        return self.total_seconds < other.total_seconds

    def __le__(self, other: "HMSTime") -> bool:
        """Check if this HMSTime object is less than or equal to another."""
        return self.total_seconds <= other.total_seconds

    def __gt__(self, other: "HMSTime") -> bool:
        """Check if this HMSTime object is greater than another."""
        return self.total_seconds > other.total_seconds

    def __ge__(self, other: "HMSTime") -> bool:
        """Check if this HMSTime object is greater than or equal to another."""
        return self.total_seconds >= other.total_seconds

    def __ne__(self, other: object) -> bool:
        """Check if two HMSTime objects are not equal."""
        if not isinstance(other, HMSTime):
            return NotImplemented
        return self.total_seconds != other.total_seconds

    @classmethod
    def from_seconds(cls, total_seconds: int) -> "HMSTime":
        """Create an HMSTime object from a total number of seconds.

        Args:
        ----
            total_seconds (int): The total number of seconds.

        Returns:
        -------
            HMSTime: The corresponding HMSTime object.

        """
        instance = cls.__new__(cls)
        instance.total_seconds = total_seconds
        return instance

    @classmethod
    def sum(cls, times: Iterable["HMSTime"]) -> "HMSTime":
        """Sum multiple HMSTime objects and return a new HMSTime object.

        Args:
        ----
            times (Iterable[HMSTime]): An iterable of HMSTime objects to sum.

        Returns:
        -------
            HMSTime: The sum of all the times.

        Raises:
        ------
            TypeError: If the input is not iterable or contains non-HMSTime objects.

        """
        try:
            total_seconds = 0
            for time_obj in times:
                if not isinstance(time_obj, cls):
                    raise TypeError(f"All items must be HMSTime objects, got: {type(time_obj).__name__}")
                total_seconds += time_obj.total_seconds
            return cls.from_seconds(total_seconds)
        except TypeError as e:
            if "not iterable" in str(e):
                raise TypeError("Input must be an iterable of HMSTime objects") from e
            raise

    @staticmethod
    def _parse_time_string(time_str: str) -> int:
        """Parse a time string and return the total number of seconds.

        Args:
        ----
            time_str (str): Time string to parse.

        Returns:
        -------
            int: Total number of seconds represented by the string.

        Raises:
        ------
            NotTimeStringError: If input is not a string.
            InvalidTimeFormatError: If the string format is invalid.

        """
        if not isinstance(time_str, str):
            raise NotTimeStringError(time_str)

        match = re.fullmatch(r"(-)?(\d+):(\d{1,2})(?::(\d{1,2}))?", time_str)
        if not match:
            raise InvalidTimeFormatError(time_str)
        neg, hh, mm, ss = match.groups()
        hh = int(hh)
        mm = int(mm)
        ss = int(ss) if ss is not None else 0

        total = hh * 3600 + mm * 60 + ss
        return -total if neg else total

    def to_seconds(self) -> int:
        """Return the total number of seconds represented by this HMSTime object."""
        return self.total_seconds

    def to_minutes(self) -> float:
        """Return the total number of minutes represented by this HMSTime object."""
        return self.total_seconds / 60

    def to_hours(self) -> float:
        """Return the total number of hours represented by this HMSTime object."""
        return self.total_seconds / 3600

    def to_tuple(self) -> tuple[int, int, int]:
        """Return the time as a tuple of (hours, minutes, seconds)."""
        total = abs(self.total_seconds)
        hh = total // 3600
        mm = (total % 3600) // 60
        ss = total % 60
        return (hh, mm, ss)

    def to_dict(self) -> dict[str, int]:
        """Return the time as a dictionary with keys 'hh', 'mm', and 'ss'."""
        hh, mm, ss = self.to_tuple()
        return {"hh": hh, "mm": mm, "ss": ss}
