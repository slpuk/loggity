class Logger:
    """Simple, beautiful logger"""
        
    def _log(self, header, message):
        """Internal log method"""
        print(f"{header}:\t{message}")
    
    def info(self, message):
        """Informational message"""
        self._log('INFO', message)
    
    def warn(self, message):
        """Warning message"""
        self._log('WARN', message)
    
    def error(self, message):
        """Error message"""
        self._log('ERROR', message)
    
    def debug(self, message):
        """Debug message"""
        self._log('DEBUG', message)
    
    def success(self, message):
        """SUCCS message"""
        self._log('SUCCS', message)
    
    def custom(self, header, message):
        """
        Custom log with any header
        
        Example:
            log.custom("PING", "Device responded")
        """
        self._log(header, message)