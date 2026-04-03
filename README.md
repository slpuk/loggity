# Loggity
> A simple, beautiful logger with a clean and intuitive interface

![Version](https://img.shields.io/badge/version-0.6.0-blue?style=for-the-badge)
![Status](https://img.shields.io/badge/status-alpha-orange?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)
![Python](https://img.shields.io/badge/python-3.7+-blue?style=for-the-badge&logo=python&logoColor=white)

## Features

- **Colorful output**: Beautiful ANSI colors for different log levels
- **Flexible timestamps**: Custom timestamp formats using `strftime`
- **File logging**: Write logs to files with automatic session separation
- **Context logging**: Hierarchical contexts for better log organization
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
log.info("Application started")                 # Blue
log.success("Database connected successfully")  # Green
log.warn("Disk space running low")              # Yellow
log.error("Failed to send email")               # Red
log.debug("Cache miss for key: user_123")       # White
```

## Context Logging

Contexts help you organize logs by adding hierarchical information to each message. Perfect for tracking execution flow in complex applications.

### Basic Context Usage

```python
from loggity import Logger

# Create logger with initial context
log = Logger(context="Server")

log.info("Started")              # INFO (Server): Started

# Change context at runtime
log.set_context("Database")
log.info("Connected")            # INFO (Database): Connected

# Disable context
log.set_context("")
log.info("Ready")                # INFO: Ready
```

### Nested Contexts with Context Manager

Use `with_context()` for temporary context changes:

```python
from loggity import Logger

log = Logger(context="Server")

log.info("Started")                 # INFO (Server): Started

with log.with_context("HTTP"):
    log.info("Request received")    # INFO (Server.HTTP): Request received
    
    with log.with_context("DB"):
        log.info("Query executed")  # INFO (Server.HTTP.DB): Query executed
    
    log.info("Response sent")       # INFO (Server.HTTP): Response sent

log.info("Shutdown")                # INFO (Server): Shutdown
```

### Manual Context Stack Management

For advanced use cases, manage the context stack directly:

```python
log = Logger(context="Server")

# Push contexts manually
log.push_context("API")
log.push_context("v1")
log.info("Processing")              # INFO (Server.API.v1): Processing

# Pop contexts
log.pop_context()                   # Removes 'v1'
log.info("Version handled")         # INFO (Server.API): Version handled

log.pop_context()                   # Removes 'API'
log.info("Done")                    # INFO (Server): Done
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

# Apply configuration with initial context
log = Logger(config=config, context="Server")

log.info("Server started")
# Console: [14:30:22] INFO (Server):    Server started
# File:    [14:30:22] INFO:    Server started (no colors, no context in file)
```

### File Logging

When file logging is enabled, Loggity automatically:

- Creates/opens the log file in append mode
- Adds a session separator when logger starts
- Writes all logs without ANSI color codes (contexts are omitted for cleaner files)
- Handles file write errors gracefully

Example log file content:
```
=== Started at 2024-01-15 14:30:22.123456
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

#### Context Management

| Method | Description | Example |
|--------|-------------|---------|
| `set_context(ctx)` | Replace entire context stack | `log.set_context("Server")` |
| `push_context(ctx)` | Add context to stack | `log.push_context("API")` |
| `pop_context()` | Remove last context from stack | `ctx = log.pop_context()` |
| `get_context()` | Get current context string | `ctx = log.get_context()` |
| `with_context(ctx)` | Context manager for temporary context | `with log.with_context("DB"):` |

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
), context="Security")

# Custom log types with any color
log.custom("AUDIT", Colors.MAGENTA, "User admin performed deletion")
# [14:30:22] AUDIT (Security):    User admin performed deletion

log.custom("METRIC", Colors.CYAN, "Response time: 245ms")
# [14:30:22] METRIC (Security):    Response time: 245ms
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

### Web Server Logger with Contexts

```python
from loggity import Logger, Colors, LoggerConfig

config = LoggerConfig(
    colored=True,
    timestamps=True,
    timeformat="%H:%M:%S.%f",
    file="server.log"
)

log = Logger(config=config, context="Server")

# Main server context
log.info("Starting on port 8000")

# Handle a request with nested contexts
def handle_request(request_id):
    with log.with_context(f"Request-{request_id}"):
        log.info("Received request")
        
        with log.with_context("Auth"):
            log.info("Checking credentials")
            # Auth logic here
        
        with log.with_context("Database"):
            log.info("Executing query")
            # Database query here
        
        with log.with_context("Response"):
            log.info("Sending response")
        
        log.info("Request completed")

handle_request(123)
handle_request(456)

log.info("Server shutdown")
```

### Microservices Logger

```python
from loggity import Logger, LoggerConfig

# Service-specific logger
def create_service_logger(service_name):
    config = LoggerConfig(
        colored=True,
        timestamps=True,
        timeformat="%Y-%m-%d %H:%M:%S",
        file=f"{service_name}.log"
    )
    return Logger(config=config, context=service_name)

# Create loggers for different services
auth_logger = create_service_logger("AuthService")
payment_logger = create_service_logger("PaymentService")
notification_logger = create_service_logger("NotificationService")

# Use them with contexts
auth_logger.info("User login attempt")
with auth_logger.with_context("TokenValidation"):
    auth_logger.debug("Validating JWT token")

payment_logger.info("Processing payment")
with payment_logger.with_context("Stripe"):
    payment_logger.info("Creating charge")
```

### Development vs Production Configuration

```python
from loggity import Logger, LoggerConfig
import os

environment = os.getenv("ENV", "development")

if environment == "development":
    config = LoggerConfig(
        colored=True,
        timestamps=True,
        timeformat="%H:%M:%S.%f",
        file="dev.log"
    )
    log = Logger(config=config, context="Dev")
    log.debug("Debug mode enabled")
else:
    config = LoggerConfig(
        colored=False,
        timestamps=True,
        timeformat="%Y-%m-%d %H:%M:%S",
        file="prod.log"
    )
    log = Logger(config=config, context="Prod")

log.info(f"Running in {environment} mode")
```

### Full-Featured Example

```python
from loggity import Logger, Colors, LoggerConfig

config = LoggerConfig(
    colored=True,
    timestamps=True,
    timeformat="%H:%M:%S.%f",
    file="application.log"
)

log = Logger(config=config, context="Server")

# Basic usage with context
log.info("Server started on port 8000")
# [14:30:22.123456] INFO (Server):    Server started on port 8000

log.warn("Config file not found, using defaults")
# [14:30:23.123456] WARN (Server):    Config file not found, using defaults

# Change context
log.set_context("Database")
log.error("Failed to connect to database")
# [14:30:24.123456] ERROR (Database):    Failed to connect to database

# Change timestamp format
log.set_format("%H%M%S")
log.debug("Received payload: {'temp': 23.5}")
# [143022] DEBUG (Database):    Received payload: {'temp': 23.5}

# Disable timestamps
log.set_format("")
log.success("Database migration completed")
# SUCCESS (Database):    Database migration completed

# Custom logging with context
log.custom("METRIC", Colors.MAGENTA, "Response time: 245ms")
# METRIC (Database):    Response time: 245ms

# Nested contexts
with log.with_context("Query"):
    log.info("SELECT * FROM users")
    # INFO (Database.Query):    SELECT * FROM users

# Plain logger without any formatting
plain_config = LoggerConfig(colored=False, timestamps=False)
plain_log = Logger(config=plain_config)
plain_log.info("Plain log")
# INFO:    Plain log
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

## Output Format Summary

### Console Output (with colors and contexts)
```
[14:30:22] INFO (Server):    Started
[14:30:22] INFO (Server.HTTP):    Request received
[14:30:22] INFO (Server.HTTP.DB):    Query executed
[14:30:22] INFO (Server.HTTP):    Response sent
[14:30:22] INFO (Server):    Shutdown
```

### File Output (no colors, no contexts)
```
=== Started at 2024-01-15 14:30:22.123456
[14:30:22] INFO (Server):    Started
[14:30:22] INFO (Server.HTTP):    Request received
[14:30:22] INFO (Server.HTTP.DB):    Query executed
[14:30:22] INFO (Server.HTTP):    Response sent
[14:30:22] INFO (Server):    Shutdown
```

## License

This project is licensed under the [MIT License](https://github.com/slpuk/loggity/blob/main/LICENSE).
