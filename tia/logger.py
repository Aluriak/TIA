# -*- coding: utf-8 -*-

from tia              import info
from logging.handlers import RotatingFileHandler
import logging



# Logging
LOGGER_NAME             = info.PACKAGE_NAME
LOG_LEVEL               = logging.DEBUG
DIR_LOGS                = 'logs/'



def logger(name=LOGGER_NAME, logfilename=None):
    """Return logger of given name, without initialize it.

    Equivalent of logging.getLogger() call.
    """
    return logging.getLogger(name)



_logger = logging.getLogger(LOGGER_NAME)
_logger.setLevel(LOG_LEVEL)

# log file
formatter    = logging.Formatter(
    '%(asctime)s :: %(levelname)s :: %(message)s'
)
file_handler = RotatingFileHandler(
    DIR_LOGS + LOGGER_NAME + '.log',
    'a', 1000000, 1
)
file_handler.setLevel(LOG_LEVEL)
file_handler.setFormatter(formatter)
_logger.addHandler(file_handler)

# terminal log
stream_handler = logging.StreamHandler()
formatter      = logging.Formatter('%(levelname)s: %(message)s')
stream_handler.setFormatter(formatter)
stream_handler.setLevel(LOG_LEVEL)
_logger.addHandler(stream_handler)


def stream_handlers():
    return (_ for _ in _logger.handlers
            if _.__class__ is logging.StreamHandler
           )

def log_level(level):
    """Set terminal log level to given one"""
    for handler in stream_handlers():
        handler.setLevel(level.upper())

