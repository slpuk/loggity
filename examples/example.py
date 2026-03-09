from loggity import Logger, Colors

log = Logger(colored=True, timestamps=True)

# Basic usage with timestamps
log.info("Server started on port 8000")
log.warn("Config file not found, using defaults")
log.error("Failed to connect to database")
log.debug("Received payload: {'temp': 23.5}")
log.success("Database migration completed")

# Custom usage
log.custom("METRIC", Colors.MAGENTA, "Response time: 245ms")

# Plain without timestamp
plain_log = Logger(colored=False, timestamps=False)
plain_log.info("Plain log")