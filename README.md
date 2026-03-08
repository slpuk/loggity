# Loggity
> A simple, beautiful logger with a clean and intuitive interface

![Version](https://img.shields.io/badge/version-0.2.0-blue?style=for-the-badge)
![Status](https://img.shields.io/badge/status-alpha-orange?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)
![Python](https://img.shields.io/badge/python-3.7+-blue?style=for-the-badge&logo=python&logoColor=white)

## Features

- **Colorful output**: Beautiful ANSI colors for different log levels
- **Simple API**: Just create a logger and start logging
- **Multiple log levels**: INFO (blue), WARN (yellow), ERROR (red), DEBUG (white), SUCCESS (green)
- **Custom headers**: Create your own log types with custom colors
- **Lightweight**: Pure Python, no external dependencies
- **Clean formatting**: Consistent spacing and aligned output
- **Toggle colors**: Enable/disable colored output as needed

## Installation

```bash
pip install loggity
```

## Quick Start

```python
from loggity import Logger

# Create a logger instance (colors enabled by default)
log = Logger()

# Start logging with beautiful colors
log.info("Application started")                 # Blue
log.success("Database connected successfully")  # Green
log.warn("Disk space running low")              # Yellow
log.error("Failed to send email")               # Red
log.debug("Cache miss for key: user_123")       # White
```

## API Reference

### Basic Methods

All basic methods come with predefined colors:

| Method | Color | Description | Example |
|--------|-------|-------------|---------|
| `info(message)` | Blue | Informational messages | `log.info("Server started on port 8080")` |
| `warn(message)` | Yellow | Warning messages | `log.warn("API rate limit at 90%")` |
| `error(message)` | Red | Error messages | `log.error("Connection timeout")` |
| `debug(message)` | White | Debug messages | `log.debug("Request payload: {...}")` |
| `success(message)` | Green | Success messages | `log.success("Data exported")` |

### Custom Logging with Colors

Create logs with custom headers and colors using the `Colors` class:

```python
from loggity import Logger, Colors

log = Logger()

# Custom log types with any color
log.custom("AUDIT", Colors.MAGENTA, "User admin performed deletion")
log.custom("METRIC", Colors.CYAN, "Response time: 245ms")
log.custom("SECURITY", Colors.RED, "Failed login attempt from 192.168.1.100")
log.custom("PERFORMANCE", Colors.BLUE, "Query executed in 0.3s")
log.custom("CACHE", Colors.GREEN, "Hit ratio: 94%")
```

### Available Colors

The `Colors` class provides the following ANSI color codes:

| Color | Usage |
|-------|-------|
| `Colors.BLACK` | `log.custom("BLACK", Colors.BLACK, "message")` |
| `Colors.RED` | `log.custom("RED", Colors.RED, "message")` |
| `Colors.GREEN` | `log.custom("GREEN", Colors.GREEN, "message")` |
| `Colors.YELLOW` | `log.custom("YELLOW", Colors.YELLOW, "message")` |
| `Colors.BLUE` | `log.custom("BLUE", Colors.BLUE, "message")` |
| `Colors.MAGENTA` | `log.custom("MAGENTA", Colors.MAGENTA, "message")` |
| `Colors.CYAN` | `log.custom("CYAN", Colors.CYAN, "message")` |
| `Colors.WHITE` | `log.custom("WHITE", Colors.WHITE, "message")` |

### Configuration

#### Disable Colors

If you need to disable colored output:

```python
# Create logger without colors
log = Logger(colored=False)

# All output will be plain text
log.info("This will be without colors")
log.custom("PLAIN", Colors.RED, "Color parameter is ignored")  # Color is ignored when colored=False
```

## Output Format

### Colored Output
When colors are enabled (`colored=True`, default), the header appears in its designated color:
```
INFO:        Application started
SUCCESS:     Database connected successfully
WARN:        Disk space running low
ERROR:       Failed to send email
DEBUG:       Cache miss for key: user_123
AUDIT:       User admin performed deletion
METRIC:      Response time: 245ms
```

### Plain Output
When colors are disabled (`colored=False`):
```
INFO:        Application started
SUCCESS:     Database connected successfully
WARN:        Disk space running low
ERROR:       Failed to send email
DEBUG:       Cache miss for key: user_123
AUDIT:       User admin performed deletion
METRIC:      Response time: 245ms
```

## License

This project is licensed under the [MIT License](LICENSE).
