# Loggity
> A simple, beautiful logger with a clean and intuitive interface

![Version](https://img.shields.io/badge/version-0.3.1-blue?style=for-the-badge)
![Status](https://img.shields.io/badge/status-alpha-red?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)
![Python](https://img.shields.io/badge/python-3.7+-blue?style=for-the-badge&logo=python&logoColor=white)

## Features

- **Colorful output**: Beautiful ANSI colors for different log levels
- **Timestamps**: Optional timestamps in `HH:MM:SS.ms` format
- **Simple API**: Just create a logger and start logging
- **Multiple log levels**: INFO (blue), WARN (yellow), ERROR (red), DEBUG (white), SUCCESS (green)
- **Custom headers**: Create your own log types with custom colors
- **Lightweight**: Pure Python, no external dependencies
- **Clean formatting**: Consistent spacing and aligned output
- **Toggle features**: Enable/disable colors and timestamps independently

## Installation

```bash
pip install loggity
```

## Quick Start

```python
from loggity import Logger

# Create a logger instance with default settings (colors enabled, no timestamps)
log = Logger()

# Start logging with beautiful colors
log.info("Application started")              # Blue
log.success("Database connected successfully") # Green
log.warn("Disk space running low")           # Yellow
log.error("Failed to send email")             # Red
log.debug("Cache miss for key: user_123")     # White
```

## Configuration

### With Timestamps

Enable timestamps to track when events occur:

```python
from loggity import Logger

# Enable both colors and timestamps
log = Logger(colored=True, timestamps=True)

# Output will include timestamps
log.info("Server started on port 8000")
# [143022] INFO:    Server started on port 8000
log.warn("Config file not found, using defaults")
# [143022] WARN:    Config file not found, using defaults
```

### Plain Output (No Colors)

Perfect for logging to files or environments that don't support ANSI colors:

```python
# Disable colors, keep timestamps
log = Logger(colored=False, timestamps=True)

# Output without colors
log.info("Writing to log file")
# [143022] INFO:    Writing to log file
```

### Minimal Output

Disable both colors and timestamps for clean, simple output:

```python
# Plain logger without any formatting
log = Logger(colored=False, timestamps=False)

log.info("Clean output")
# INFO:    Clean output
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

log = Logger(timestamps=True)

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

## Output Format Examples

### Full Features (Colors + Timestamps)
```python
log = Logger(colored=True, timestamps=True)
log.info("Server started")
log.error("Connection failed")
```
Output:
```
[17:37:33.331522] INFO:    Server started
[17:37:33.331591] ERROR:   Connection failed
```

### Colors Only
```python
log = Logger(colored=True, timestamps=False)
log.success("Task completed")
```
Output:
```
SUCCESS:    Task completed
```

### Timestamps Only
```python
log = Logger(colored=False, timestamps=True)
log.warn("Low disk space")
```
Output:
```
[17:37:33.331522] WARN:    Low disk space
```

### Plain
```python
log = Logger(colored=False, timestamps=False)
log.custom("TEST", Colors.RED, "Color is ignored")
```
Output:
```
TEST:    Color is ignored
```

## Complete Example

```python
from loggity import Logger, Colors

# Logger with colors and timestamps
log = Logger(colored=True, timestamps=True)

# Basic usage
log.info("Server started on port 8000")
log.warn("Config file not found, using defaults")
log.error("Failed to connect to database")
log.debug("Received payload: {'temp': 23.5}")
log.success("Database migration completed")

# Custom usage
log.custom("METRIC", Colors.MAGENTA, "Response time: 245ms")

# Plain logger without any formatting
plain_log = Logger(colored=False, timestamps=False)
plain_log.info("Plain log entry")
```

## License

This project is licensed under the [MIT License](https://github.com/slpuk/loggity/blob/main/LICENSE).
