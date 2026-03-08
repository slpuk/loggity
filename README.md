# Loggity
> A simple, beautiful logger with a clean and intuitive interface

![Protocol Version](https://img.shields.io/badge/version-0.1.0-blue?style=for-the-badge)
![Development Status](https://img.shields.io/badge/status-alpha-red?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)
![Python](https://img.shields.io/badge/python-3.7+-blue?style=for-the-badge&logo=python&logoColor=white)

## Features

- **Simple API**: Just create a logger and start logging
- **Multiple log levels**: INFO, WARN, ERROR, DEBUG, SUCCESS
- **Custom headers**: Create your own log types
- **Minimal dependencies**: Pure Python, no external packages required
- **Clean output**: Formatted logs with consistent spacing

## Installation

```bash
pip install loggity
```

## Quick Start

```python
from loggity import Logger

# Create a logger instance
log = Logger()

# Start logging
log.info("Application started")
log.success("Database connected successfully")
log.warn("Disk space running low")
log.error("Failed to send email")
log.debug("Cache miss for key: user_123")
```

## API Reference

### Basic Methods

| Method | Description | Example |
|--------|-------------|---------|
| `info(message)` | Informational messages | `log.info("Server started on port 8080")` |
| `warn(message)` | Warning messages | `log.warn("API rate limit at 90%")` |
| `error(message)` | Error messages | `log.error("Connection timeout")` |
| `debug(message)` | Debug messages | `log.debug("Request payload: {...}")` |
| `success(message)` | Success messages | `log.success("Data exported")` |

### Custom Logging

Create logs with any header using the `custom()` method:

```python
# Custom log types
log.custom("AUDIT", "User admin performed deletion")
log.custom("METRIC", "Response time: 245ms")
log.custom("SECURITY", "Failed login attempt from 192.168.1.100")
log.custom("PERFORMANCE", "Query executed in 0.3s")
```

## Output Format

All logs follow a consistent format:
```
HEADER:    message
```

Examples:
```
INFO:    Application started
SUCCS:   Database connected
WARN:    Disk space low
ERROR:   Connection failed
DEBUG:   Cache miss
AUDIT:   User logged in
```

## License
This project is licensed under the [MIT License](LICENSE).