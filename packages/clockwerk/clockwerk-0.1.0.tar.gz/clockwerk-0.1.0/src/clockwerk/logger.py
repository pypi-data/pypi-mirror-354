#-------------------- Imports --------------------

import logging

from logging.handlers import RotatingFileHandler

from src.clockwerk.config import LoggerConfig

#-------------------- Logging Configuration --------------------

def setup_logger(name: str, config: LoggerConfig) -> logging.Logger:
    """
    Set ups, configures and returns a Logger-object with a given name.
    The Logger utilises a Stream Handler & optional Rotating File Handler
    """

    logger = logging.getLogger(name)
    logger.setLevel(config.log_level)

    # Returns Logger without adding additonal handlers if called multiple times
    if logger.handlers:
        return logger
    
    formatter = logging.Formatter(fmt=config.log_format, datefmt=config.date_format)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Optional file Handler
    if config.log_to_file:
        file_handler = RotatingFileHandler(
            filename=config.log_file,
            maxBytes=5 * 1024 * 1024,
            backupCount=5
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


#-------------------- Global Logging System --------------------

_logger = None

def get_logger() -> logging.Logger:
    """
    Returns the Global logger-object defined by the setup_logger configuration
    """
    global _logger
    if _logger is None:
        config = LoggerConfig(
            log_level="INFO",
            log_file="monitor.log",
            log_to_file=True  
        )
        _logger = setup_logger("MonitorSystem", config)
    return _logger