"""Simple, dependency-free logger with colors."""

from datetime import datetime
from dataclasses import dataclass
from typing import Optional


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

    def __init__(self, config: Optional[LoggerConfig] = None):
        """Initialize logger with given configuration.
        
        Args:
            config: Logger configuration. If None, defaults are used.
        """
        self.config = config or LoggerConfig()
        self.colored = self.config.colored
        self.timestamps = self.config.timestamps
        self._time_format = self.config.timeformat
        self._log_file = self.config.file

        if self._log_file and len(self._log_file) > 0:
            try:
                with open(self._log_file, "a", encoding="utf-8") as file:
                    file.write(f"\n=== Started at {datetime.now()}\n")
            except Exception as error:
                self.custom("LOGGITY", Colors.RED, error)

    def _get_timestamp(self) -> str:
        """Generate timestamp string based on configured format.
        
        Returns:
            Formatted timestamp string or empty string if timestamps disabled.
        """
        if not self.timestamps:
            return ""
            
        try:
            if self._time_format:
                return f"[{datetime.now().strftime(self._time_format)}] "
            return ""
        except Exception as error:
            self.custom("LOGGITY", Colors.RED, error)
            return ""

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
        except Exception as error:
            self.custom("LOGGITY", Colors.RED, error)

    def _log(self, header: str, color: str, message: str) -> None:
        """Internal method for unified logging logic.
        
        This method centralizes all logging to ensure consistency between
        console output and file writing.
        
        Args:
            header: Log level or custom header.
            color: ANSI color code for the header.
            message: Log message content.
        """
        timestamp = self._get_timestamp()
        
        if self.colored:
            log_line = f"{timestamp}{color}{header}{Colors.RESET}:    \t{message}"
        else:
            log_line = f"{timestamp}{header}:    \t{message}"
            
        print(log_line)
        self._write_to_file(f"{timestamp}{header}:    \t{message}")

    def set_format(self, time_format: str) -> None:
        """Change the timestamp format at runtime.
        
        Args:
            time_format: New format string for datetime.strftime().
            *Empty string disables timestamps.*
        
        Example:
        ```python
            log.set_format("%H:%M:%S")  # Show only time
            log.set_format("")  # Disable timestamps
        ```
        """
        self._time_format = time_format if time_format else None
        self.timestamps = bool(time_format)

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