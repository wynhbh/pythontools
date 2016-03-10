import logging
import logging.config

logging.config.fileConfig("logging.conf")

logger = logging.getLogger("simpleExample")

logger.debug("debug message")
logger.info("info message")
logger.warn("warn message")
logger.error("error message")
logger.critical("ciritical message")

