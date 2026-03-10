# Loggity
> A simple, beautiful logger with a clean and intuitive interface

![Version](https://img.shields.io/badge/version-0.4.0-blue?style=for-the-badge)
![Status](https://img.shields.io/badge/status-alpha-orange?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)
![Python](https://img.shields.io/badge/python-3.7+-blue?style=for-the-badge&logo=python&logoColor=white)

## Features

- **Colorful output**: Beautiful ANSI colors for different log levels
- **Flexible timestamps**: Custom timestamp formats using `strftime`
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

### Basic Configuration

```python
from loggity import Logger, LoggerConfig

# Create configuration
config = LoggerConfig(
    colored=True,
    timestamps=True,
    timeformat="%H:%M:%S"  # 24-hour format: 14:30:22
)

# Apply configuration
log = Logger(config=config)

log.info("Server started")
# [14:30:22] INFO:    Server started
```

### Timestamp Formats

The `timeformat` parameter accepts any valid `strftime` format string:

```python
# Various timestamp formats
formats = {
    "simple": "%H%M%S",           # 143022
    "readable": "%H:%M:%S",        # 14:30:22
    "with_ms": "%H:%M:%S.%f",      # 14:30:22.123456
    "date_and_time": "%Y-%m-%d %H:%M:%S",  # 2024-01-15 14:30:22
    "compact": "%y%m%d_%H%M%S",    # 240115_143022
}

for name, fmt in formats.items():
    config = LoggerConfig(timestamps=True, timeformat=fmt)
    log = Logger(config=config)
    log.info(f"Testing {name} format")
```

### Runtime Format Changes

Change the timestamp format dynamically using `set_format()`:

```python
log = Logger(config=LoggerConfig(timestamps=True, timeformat="%H:%M:%S"))

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

log = Logger(config=LoggerConfig(timestamps=True, timeformat="%H:%M:%S"))

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

### Basic Usage with Different Formats

```python
from loggity import Logger, Colors, LoggerConfig

# Logger with milliseconds timestamp
config = LoggerConfig(
    colored=True,
    timestamps=True,
    timeformat="%H:%M:%S.%f"
)
log = Logger(config=config)

log.info("Server started on port 8000")
# [14:30:22.123456] INFO:    Server started on port 8000

log.warn("Config file not found, using defaults")
# [14:30:22.123789] WARN:    Config file not found, using defaults

# Change to compact format
log.set_format("%H%M%S")
log.error("Failed to connect to database")
# [143022] ERROR:    Failed to connect to database

# Disable timestamps
log.set_format("")
log.success("Database migration completed")
# SUCCESS:    Database migration completed
```

### Custom Headers with Colors

```python
log.custom("METRIC", Colors.MAGENTA, "Response time: 245ms")
# [14:30:22] METRIC:    Response time: 245ms
```

### Plain Logger (No Colors, No Timestamps)

```python
plain_config = LoggerConfig(colored=False, timestamps=False)
plain_log = Logger(config=plain_config)

plain_log.info("Plain log entry")
# INFO:    Plain log entry
```

### Multiple Loggers with Different Configurations

```python
from loggity import Logger, LoggerConfig

# Development logger with detailed timestamps
dev_config = LoggerConfig(
    colored=True,
    timestamps=True,
    timeformat="%H:%M:%S.%f"
)
dev_log = Logger(config=dev_config)

# Production logger with minimal output
prod_config = LoggerConfig(colored=False, timestamps=False)
prod_log = Logger(config=prod_config)

dev_log.debug("Processing request...")
prod_log.info("Request completed")
```

## Error Handling

The logger gracefully handles invalid timestamp formats:

```python
log = Logger(config=LoggerConfig(timestamps=True, timeformat="%invalid"))

# Invalid format triggers a custom error log
log.info("This will still work")  
# [LOGGITY:    ERROR] Invalid format string
# INFO:    This will still work
```

## License

This project is licensed under the [MIT License](https://github.com/slpuk/loggity/blob/main/LICENSE).
