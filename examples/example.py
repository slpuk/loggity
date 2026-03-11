from loggity import Logger, Colors, LoggerConfig

config = LoggerConfig(
    colored=True, timestamps=True, timeformat="%H:%M:%S.%f", file="logger.log"
)

log = Logger(config=config)

# Basic usage
log.info("Server started on port 8000")
log.warn("Config file not found, using defaults")
log.set_format("%H%M%S")
log.error("Failed to connect to database")
log.debug("Received payload: {'temp': 23.5}")
log.set_format("")
log.success("Database migration completed")

# Custom usage
log.custom("METRIC", Colors.MAGENTA, "Response time: 245ms")

# Plain
plain_config = LoggerConfig(colored=False, timestamps=False, timeformat=None, file=None)
plain_log = Logger(config=plain_config)
plain_log.info("Plain log")
