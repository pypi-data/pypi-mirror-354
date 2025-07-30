# simple-shortcuts

Simple, intuitive abstractions for common Python tasks.

## Status

🚧 **Early Development** – APIs may change

## Contributing

Feedback and abstraction requests are welcome! Open an issue to suggest new shortcuts or improvements.

## License

[Apache 2.0](LICENSE)

## Installation

```bash
pip install simple-shortcuts
```

## Samples from the `date` module

```python
from shortcuts.date import time_in, time_ago, time_now, Config


# Get local time now
now = time_now()

# Get utc time now
utc = time_now(utc=True)

# Get timezone aware value
tz_aware = time_now(naive=False)

# Get time in x hours
future = time_in(hours=2)

# Combine intervals
future = time_in(seconds=5, minutes=3, hours=1)

# Get time in the past
past = time_ago(seconds=25, minutes=2, utc=True, naive=False)

# Globally override naive and utc defaults
Config.naive = False
Config.utc = True
```
