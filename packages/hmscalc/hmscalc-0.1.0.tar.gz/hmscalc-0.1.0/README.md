# hmscalc

A lightweight Python library for performing arithmetic on time values formatted as `HH:MM` or `HH:MM:SS`.

## 🚀 Features

- Supports time addition and subtraction
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

```python
from hmscalc import HMSTime

a = HMSTime("1:30:15")
b = HMSTime("2:15:45")

print(a + b)            # "3:46:00"
print(a - b)            # "-0:45:30"
print(a.to_seconds())   # 5415
print(a.to_tuple())     # (1, 30, 15)
print(a.to_dict())      # {'hh': 1, 'mm': 30, 'ss': 15}
```

## 🔍 Examples

```python
HMSTime("2:30") + HMSTime("1:45")     # "4:15:00"
HMSTime("1:00:30") - HMSTime("0:30")  # "0:30:30"
HMSTime("0:00") - HMSTime("0:01")     # "-0:01:00"
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
