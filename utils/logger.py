"""Logging Utilities"""

import sys
from loguru import logger
from config import LOGGING_CONFIG


def setup_logger():
    """Setup logger configuration"""
    logger.remove()
    
    # Console logging
    logger.add(
        sys.stderr,
        level=LOGGING_CONFIG['level'],
        format=LOGGING_CONFIG['format']
    )
    
    # File logging
    logger.add(
        LOGGING_CONFIG['log_file'],
        level=LOGGING_CONFIG['level'],
        format=LOGGING_CONFIG['format'],
        rotation="500 MB",
    )
    
    return logger