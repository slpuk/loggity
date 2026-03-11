# Loggity
> A simple, beautiful logger with a clean and intuitive interface

![Version](https://img.shields.io/badge/version-0.5.0-blue?style=for-the-badge)
![Status](https://img.shields.io/badge/status-alpha-orange?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)
![Python](https://img.shields.io/badge/python-3.7+-blue?style=for-the-badge&logo=python&logoColor=white)

## Features

- **Colorful output**: Beautiful ANSI colors for different log levels
- **Flexible timestamps**: Custom timestamp formats using `strftime`
- **File logging**: Write logs to files with automatic session separation
- **Simple API**: Just create a logger and start logging
- **Multiple log levels**: INFO (blue), WARN (yellow), ERROR (red), DEBUG (white), SUCCESS (green)
- **Custom headers**: Create your own log types with custom colors
- **Lightweight**: Pure Python, no external dependencies
- **Clean formatting**: Consistent spacing and aligned output
- **Dataclass config**: Type-safe configuration with `LoggerConfig`
- **Runtime formatting**: Change timestamp format on the fly with `set_format()`

## Installation

```bash
pip install loggity
```

## Quick Start

```python
from loggity import Logger

# Create a logger instance with default settings
log = Logger()

# Start logging with beautiful colors
log.info("Application started")              # Blue
log.success("Database connected successfully") # Green
log.warn("Disk space running low")           # Yellow
log.error("Failed to send email")             # Red
log.debug("Cache miss for key: user_123")     # White
```

## Configuration

Loggity uses a dataclass-based configuration system for type-safe and flexible setup:

### LoggerConfig Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `colored` | `bool` | `True` | Enable/disable ANSI colors |
| `timestamps` | `bool` | `False` | Enable/disable timestamps |
| `timeformat` | `str` or `None` | `None` | `strftime` format string (requires `timestamps=True`) |
| `file` | `str` or `None` | `None` | Path to log file (enables file logging) |

### Basic Configuration

```python
from loggity import Logger, LoggerConfig

# Create configuration with timestamps and file logging
config = LoggerConfig(
    colored=True,
    timestamps=True,
    timeformat="%H:%M:%S",  # 24-hour format: 14:30:22
    file="app.log"          # Write logs to app.log
)

# Apply configuration
log = Logger(config=config)

log.info("Server started")
# Console: [14:30:22] INFO:    Server started
# File:    [14:30:22] INFO:    Server started (no colors)
```

### File Logging

When file logging is enabled, Loggity automatically:

- Creates/opens the log file in append mode
- Adds a session separator when logger starts
- Writes all logs without ANSI color codes
- Handles file write errors gracefully

Example log file content:
```
=== Started at 2026-03-11 19:30:00.123456
[14:30:22] INFO:    Server started on port 8000
[14:30:23] WARN:    Config file not found, using defaults
[14:30:24] ERROR:   Failed to connect to database
```

### Timestamp Formats

The `timeformat` parameter accepts any valid `strftime` format string:

```python
# Various timestamp formats
formats = {
    "simple": "%H%M%S",                    # 143022
    "readable": "%H:%M:%S",                 # 14:30:22
    "with_ms": "%H:%M:%S.%f",               # 14:30:22.123456
    "date_and_time": "%Y-%m-%d %H:%M:%S",   # 2024-01-15 14:30:22
    "compact": "%y%m%d_%H%M%S",             # 240115_143022
}

for name, fmt in formats.items():
    config = LoggerConfig(timestamps=True, timeformat=fmt, file="test.log")
    log = Logger(config=config)
    log.info(f"Testing {name} format")
```

### Runtime Format Changes

Change the timestamp format dynamically using `set_format()`:

```python
log = Logger(config=LoggerConfig(
    timestamps=True,
    timeformat="%H:%M:%S",
    file="app.log"
))

log.info("Starting process")        # [14:30:22] INFO:    Starting process

# Switch to compact format
log.set_format("%H%M%S")
log.info("Processing data")          # [143022] INFO:    Processing data

# Disable timestamps
log.set_format("")                   # Empty string disables timestamps
log.info("Task completed")           # INFO:    Task completed
```

## API Reference

### Logger Methods

#### Basic Methods

All basic methods come with predefined colors:

| Method | Color | Description |
|--------|-------|-------------|
| `info(message)` | Blue | Informational messages |
| `warn(message)` | Yellow | Warning messages |
| `error(message)` | Red | Error messages |
| `debug(message)` | White | Debug messages |
| `success(message)` | Green | Success messages |

#### Configuration Methods

| Method | Description | Example |
|--------|-------------|---------|
| `set_format(format_string)` | Change timestamp format at runtime | `log.set_format("%H:%M:%S")` |

#### Custom Logging

Create logs with custom headers and colors:

```python
from loggity import Logger, Colors, LoggerConfig

log = Logger(config=LoggerConfig(
    timestamps=True,
    timeformat="%H:%M:%S",
    file="audit.log"
))

# Custom log types with any color
log.custom("AUDIT", Colors.MAGENTA, "User admin performed deletion")
log.custom("METRIC", Colors.CYAN, "Response time: 245ms")
log.custom("SECURITY", Colors.RED, "Failed login attempt from 192.168.1.100")
```

### Available Colors

The `Colors` class provides ANSI color codes:

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

## Complete Examples

### Full-Featured Logger with File Output

```python
from loggity import Logger, Colors, LoggerConfig

# Logger with colors, milliseconds timestamp, and file output
config = LoggerConfig(
    colored=True,
    timestamps=True,
    timeformat="%H:%M:%S.%f",
    file="application.log"
)
log = Logger(config=config)

log.info("Server started on port 8000")
# Console: [14:30:22.123456] INFO:    Server started on port 8000
# File:    [14:30:22.123456] INFO:    Server started on port 8000

log.warn("Config file not found, using defaults")
log.error("Failed to connect to database")

# Change format dynamically
log.set_format("%H%M%S")
log.debug("Received payload: {'temp': 23.5}")

# Disable timestamps
log.set_format("")
log.success("Database migration completed")

# Custom logging
log.custom("METRIC", Colors.MAGENTA, "Response time: 245ms")
```

### Multiple Loggers with Different Configurations

```python
from loggity import Logger, LoggerConfig

# Development logger with detailed output
dev_config = LoggerConfig(
    colored=True,
    timestamps=True,
    timeformat="%H:%M:%S.%f",
    file="dev.log"
)
dev_log = Logger(config=dev_config)

# Production logger with minimal output
prod_config = LoggerConfig(
    colored=False,
    timestamps=True,
    timeformat="%Y-%m-%d %H:%M:%S",
    file="prod.log"
)
prod_log = Logger(config=prod_config)

# Audit logger for security events
audit_config = LoggerConfig(
    colored=True,
    timestamps=True,
    timeformat="%Y-%m-%d %H:%M:%S",
    file="audit.log"
)
audit_log = Logger(config=audit_config)

dev_log.debug("Processing request...")
prod_log.info("Request completed")
audit_log.custom("AUDIT", Colors.MAGENTA, "User login: admin")
```

### Plain Logger (No Colors, No Timestamps, No File)

```python
plain_config = LoggerConfig(
    colored=False,
    timestamps=False,
    file=None
)
plain_log = Logger(config=plain_config)

plain_log.info("Plain log entry")
# INFO:    Plain log entry
```

## Error Handling

The logger gracefully handles various error conditions:

```python
# Invalid timestamp format
log = Logger(config=LoggerConfig(
    timestamps=True,
    timeformat="%invalid"
))
log.info("This will still work")
# [LOGGITY:    ERROR] Invalid format string
# INFO:    This will still work

# Invalid file path
config = LoggerConfig(file="/invalid/path/log.log")
log = Logger(config=config)  # Logs error but continues
log.info("Application running")  # Still logs to console
```

## File Logging Details

When file logging is enabled:

1. **Session Separation**: Each logger instance adds a session marker
2. **No Colors**: Files contain plain text without ANSI codes
3. **UTF-8 Encoding**: Files are written with UTF-8 encoding
4. **Append Mode**: Logs are appended, existing content preserved
5. **Error Resilience**: File write errors are logged but don't crash the application

Example log file content:
```
=== Started at 2026-03-11 19:30:00.123456
[14:30:22] INFO:    Server started on port 8000
[14:30:23] WARN:    Config file not found, using defaults
[14:30:24] ERROR:   Failed to connect to database
[14:30:25] DEBUG:   Received payload: {'temp': 23.5}
[14:30:26] METRIC:  Response time: 245ms

=== Started at 2026-03-11 19:30:05.987654
[15:45:33] INFO:    Server restarted
```

## License

This project is licensed under the [MIT License](LICENSE).
