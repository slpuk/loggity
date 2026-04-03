"""Simple, dependency-free logger with colors."""

from datetime import datetime
from dataclasses import dataclass
from typing import Optional
from contextlib import contextmanager


@dataclass
class LoggerConfig:
    """Configuration for Logger instances.

    All configuration parameters are optional and have sensible defaults.
    """

    colored: bool = True
    timestamps: bool = False
    timeformat: str = None
    file: str = None


class Colors:
    """ANSI color codes for terminal output.

    These constants provide consistent color definitions across all loggers.
    Colors are only applied when colored output is enabled.
    """

    RESET = "\033[0m"
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"


class Logger:
    """Simple, beautiful logger with optional colors and file output.

    Provides standard logging levels (INFO, WARN, ERROR, DEBUG, SUCCESS)
    and custom logging with any header and color.

    Example:
    ```python
        log = Logger()
        log.info("Server started")
        log.custom("METRIC", Colors.MAGENTA, "Response time: 245ms")
    ```
    """

    _default_colors = {
        "INFO": Colors.BLUE,
        "WARN": Colors.YELLOW,
        "ERROR": Colors.RED,
        "DEBUG": Colors.WHITE,
        "SUCCESS": Colors.GREEN,
    }

    def __init__(self, config: Optional[LoggerConfig] = None, context: str = None):
        """Initialize logger with given configuration.

        Args:
            config: Logger configuration. If None, defaults are used.
            context: Initial context for the logger.
        """
        self.config = config or LoggerConfig()
        self.colored = self.config.colored
        self.timestamps = self.config.timestamps
        self._time_format = self.config.timeformat
        self._log_file = self.config.file
        self._context_stack = []
        
        if context:
            self._context_stack.append(context)

        self._write_startup_marker()

    def _write_startup_marker(self) -> None:
        """Write startup marker to log file."""
        if not self._log_file:
            return

        try:
            with open(self._log_file, "a", encoding="utf-8") as file:
                file.write(f"\n=== Started at {datetime.now()}\n")
        except IOError as error:
            self._log_error(f"Failed to write startup marker: {error}")

    def _get_timestamp(self) -> str:
        """Generate timestamp string based on configured format.

        Returns:
            Formatted timestamp string or empty string if timestamps disabled.
        """
        if not self.timestamps or not self._time_format:
            return ""

        try:
            return f"[{datetime.now().strftime(self._time_format)}] "
        except ValueError as error:
            self._log_error(f"Invalid time format: {error}")
            return ""

    def set_format(self, time_format: str) -> None:
        """Change the timestamp format at runtime.

        Args:
            time_format: New format string for datetime.strftime().
                        Empty string disables timestamps.

        Example:
        ```python
            log.set_format("%H:%M:%S")  # Show only time
            log.set_format("")  # Disable timestamps
        ```
        """
        self._time_format = time_format if time_format else None
        self.timestamps = bool(time_format)

    def _write_to_file(self, text: str) -> None:
        """Write log message to configured file.

        Args:
            text: Log message to write.
        """
        if not self._log_file:
            return

        try:
            with open(self._log_file, "a", encoding="utf-8") as file:
                file.write(text + "\n")
        except IOError as error:
            self._log_error(f"Failed to write to log file: {error}")

    def _log_error(self, message: str) -> None:
        """Internal method for logging errors that occur within the logger.

        Args:
            message: Error message to log.
        """
        print(f"[LOGGITY ERROR] {message}")

    def set_context(self, context: str) -> None:
        """Change the context at runtime.

        Args:
            context: New string for context. Empty string disables contexts.

        Example:
        ```python
            log.set_context("Server")
            log.set_context("")  # Disable context
        ```
        """
        self._context_stack = [context] if context else []

    def push_context(self, context: str) -> None:
        """Add context to stack.

        Args:
            context: Context string to push onto the stack.
        """
        self._context_stack.append(context)

    def pop_context(self) -> Optional[str]:
        """Remove and return the last context from stack.

        Returns:
            The popped context or None if stack was empty.
        """
        if self._context_stack:
            return self._context_stack.pop()
        return None

    def get_context(self) -> str:
        """Generate context string from stack.

        Returns:
            Formatted context string or empty string if no context.
        """
        if not self._context_stack:
            return ""
        return " (" + ".".join(self._context_stack) + ")"

    @contextmanager
    def with_context(self, context: str):
        """Temporarily use a context within a 'with' block.

        Args:
            context: Context to use within the block.

        Yields:
            The logger instance for chaining.

        Example:
        ```python
            with log.with_context("Database"):
                log.info("Connected")  # Shows "(Database)" in output
        ```
        """
        self.push_context(context)
        try:
            yield self
        finally:
            self.pop_context()

    def _format_log_line(self, header: str, message: str) -> str:
        """Format a log line with timestamp and context.

        Args:
            header: Log level or custom header.
            message: Log message content.

        Returns:
            Formatted log line without color codes.
        """
        timestamp = self._get_timestamp()
        context = self.get_context()
        return f"{timestamp}{header}{context}:    \t{message}"

    def _apply_color(self, text: str, color: str) -> str:
        """Apply ANSI color codes to text if colored output is enabled.

        Args:
            text: Text to colorize.
            color: ANSI color code.

        Returns:
            Colorized text or original text if colored output is disabled.
        """
        if not self.colored:
            return text
        return f"{color}{text}{Colors.RESET}"

    def _log(self, header: str, color: str, message: str) -> None:
        """Internal method for unified logging logic.

        This method centralizes all logging to ensure consistency between
        console output and file writing.

        Args:
            header: Log level or custom header.
            color: ANSI color code for the header.
            message: Log message content.
        """
        log_line = self._format_log_line(header, message)
        colored_header = self._apply_color(header, color)
        colored_log_line = self._format_log_line(colored_header, message)

        print(colored_log_line)
        self._write_to_file(log_line)

    def info(self, message: str) -> None:
        """Log informational message (blue)."""
        self._log("INFO", self._default_colors["INFO"], message)

    def warn(self, message: str) -> None:
        """Log warning message (yellow)."""
        self._log("WARN", self._default_colors["WARN"], message)

    def error(self, message: str) -> None:
        """Log error message (red)."""
        self._log("ERROR", self._default_colors["ERROR"], message)

    def debug(self, message: str) -> None:
        """Log debug message (white)."""
        self._log("DEBUG", self._default_colors["DEBUG"], message)

    def success(self, message: str) -> None:
        """Log success message (green)."""
        self._log("SUCCESS", self._default_colors["SUCCESS"], message)

    def custom(self, header: str, color: str, message: str) -> None:
        """Log with custom header and color.

        Args:
            header: Custom header text (e.g., "METRIC", "AUDIT").
            color: Any color from Colors class.
            message: Log message content.

        Example:
        ```python
            log.custom("PING", Colors.MAGENTA, "Device responded")
        ```
        """
        self._log(header, color, message)