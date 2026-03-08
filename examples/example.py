from loggity import Logger, Colors

log = Logger(colored=True)

# Basic usage
log.info("Server started on port 8000")
log.warn("Config file not found, using defaults")
log.error("Failed to connect to database")
log.debug("Received payload: {'temp': 23.5}")
log.success("Database migration completed")

# Custom usage
log.custom("METRIC", Colors.MAGENTA, "Response time: 245ms")

# Plain
plain_log = Logger(colored=False)
plain_log.debug("Plain log")