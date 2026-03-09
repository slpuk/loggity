from datetime import datetime

class Colors:
    RESET = '\033[0m'

    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'

class Logger:
    """Simple, beautiful logger with colors"""
    
    _default_colors = {
        'INFO': Colors.BLUE,
        'WARN': Colors.YELLOW,
        'ERROR': Colors.RED,
        'DEBUG': Colors.WHITE,
        'SUCCESS': Colors.GREEN,
    }
    
    def __init__(self, colored: bool = True, timestamps: bool = False):
        self.colored = colored
        self.timestamps = timestamps
        
    def _log(self, header, color, message):
        """Internal log method"""
        if self.colored:
            if self.timestamps:
                print(f"[{datetime.now().strftime('%H%M%S')}] {color}{header}{Colors.RESET}:    \t{message}")
            else:
                print(f"{color}{header}{Colors.RESET}:    \t{message}")
        else:
            if self.timestamps:
                print(f"[{datetime.now().strftime('%H%M%S')}] {header}:    \t{message}")
            else:
                print(f"{header}:    \t{message}")
    
    def info(self, message):
        """Informational message (blue)"""
        self._log('INFO', Logger._default_colors['INFO'], message)
    
    def warn(self, message):
        """Warning message (yellow)"""
        self._log('WARN', Logger._default_colors['WARN'], message)
    
    def error(self, message):
        """Error message (red)"""
        self._log('ERROR', Logger._default_colors['ERROR'], message)
    
    def debug(self, message):
        """Debug message (white)"""
        self._log('DEBUG', Logger._default_colors['DEBUG'], message)
    
    def success(self, message):
        """Success message (green)"""
        self._log('SUCCESS', Logger._default_colors['SUCCESS'], message)
    
    def custom(self, header, color, message):
        """
        Custom log with any color and header
        
        Example:
            log.custom(Colors.MAGENTA, "PING", "Device responded")
        """
        self._log(header, color, message)