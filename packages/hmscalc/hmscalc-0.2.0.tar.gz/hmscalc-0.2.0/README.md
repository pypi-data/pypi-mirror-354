# hmscalc

[![PyPI version](https://img.shields.io/pypi/v/hmscalc.svg)](https://pypi.org/project/hmscalc/)
[![Python versions](https://img.shields.io/pypi/pyversions/hmscalc.svg)](https://pypi.org/project/hmscalc/)

A lightweight Python library for performing arithmetic on time values formatted as `HH:MM` or `HH:MM:SS`.

## 🚀 Features

- Supports time addition and subtraction
- **NEW**: Sum multiple time values with `HMSTime.sum()`
- Accepts `HH:MM` and `HH:MM:SS` formatted strings
- Handles negative durations gracefully
- Converts time to seconds, minutes, hours, and dictionary/tuple formats
- Fully testable across multiple Python versions via Docker

## 🐳 Quick Start (Docker-based)

```bash
# Build the image
docker build -t hmscalc .

# Run tests across multiple Python versions
docker run --rm hmscalc ./runtests.sh

# Run lint
docker run --rm hmscalc ./lint.sh
```

## 📦 Project Structure

```
hmscalc/
├── Dockerfile         # Docker setup with pyenv and poetry
├── runtests.sh        # Runs tests on multiple Python versions
├── hmscalc/           # Source code
│   └── hms_time.py
├── tests/             # Pytest-based unit tests
├── pyproject.toml     # Poetry config
├── README.md          # This file
└── LICENSE            # MIT license
```

## 📚 Usage (inside container)

### Basic Operations

```python
from hmscalc.hms_time import HMSTime

a = HMSTime("1:30:15")
b = HMSTime("2:15:45")

print(a + b)            # "3:46:00"
print(a - b)            # "-0:45:30"
print(a.to_seconds())   # 5415
print(a.to_tuple())     # (1, 30, 15)
print(a.to_dict())      # {'hh': 1, 'mm': 30, 'ss': 15}
```

### Sum Multiple Times

```python
from hmscalc.hms_time import HMSTime

# Sum multiple time values
times = [
    HMSTime("1:30:15"),
    HMSTime("2:15:45"),
    HMSTime("0:45:30")
]
total = HMSTime.sum(times)
print(total)            # "4:31:30"

# Works with mixed formats and negative values
mixed_times = [
    HMSTime("2:30"),        # HH:MM format
    HMSTime("1:15:30"),     # HH:MM:SS format
    HMSTime("-0:30:00")     # Negative time
]
result = HMSTime.sum(mixed_times)
print(result)           # "3:15:30"

# Empty list returns zero
print(HMSTime.sum([]))  # "0:00:00"
```

## 🔍 Examples

### Basic Arithmetic
```python
HMSTime("2:30") + HMSTime("1:45")     # "4:15:00"
HMSTime("1:00:30") - HMSTime("0:30")  # "0:30:30"
HMSTime("0:00") - HMSTime("0:01")     # "-0:01:00"
```

### Sum Operations
```python
# Calculate total work time
work_sessions = [
    HMSTime("2:15:30"),  # Morning session
    HMSTime("1:45:00"),  # Afternoon session
    HMSTime("0:30:15")   # Evening session
]
total_work = HMSTime.sum(work_sessions)
print(f"Total work time: {total_work}")  # "4:30:45"

# Handle overtime calculations
regular_hours = [HMSTime("8:00:00") for _ in range(5)]  # 5 days
overtime = [HMSTime("1:30:00"), HMSTime("0:45:00")]    # 2 days overtime

total_regular = HMSTime.sum(regular_hours)  # "40:00:00"
total_overtime = HMSTime.sum(overtime)      # "2:15:00"
total_hours = total_regular + total_overtime
print(f"Total hours this week: {total_hours}")  # "42:15:00"
```

## 🧪 Running tests locally via Docker

```bash
# Build image
docker build -t hmscalc .

# Run matrix tests via pyenv + poetry
docker run --rm hmscalc ./runtests.sh
```

## 📄 License

This project is licensed under the [MIT License](LICENSE).
