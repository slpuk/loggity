from loggity import Logger, LoggerConfig

log = Logger(config=LoggerConfig(file="logger.log"), context="Server")

log = Logger(context="Server")

log.info("Started")  # INFO (Server): Started
with log.with_context("HTTP"):
    log.info("Request received")  # INFO (Server.HTTP): Request received
    with log.with_context("DB"):
        log.info("Query executed")  # INFO (Server.HTTP.DB): Query executed
    log.info("Response sent")   # INFO (Server.HTTP): Response sent
log.info("Shutdown")  # INFO (Server): Shutdown
