# src/utils/logger.py

import logging
import os
from logging.handlers import RotatingFileHandler

def get_logger(name: str) -> logging.Logger:
    """
    Returns a logger instance with a specified name. 
    The logger writes logs to both console and a rotating log file.
    
    Args:
        name (str): Name of the logger instance. Usually __name__ is passed from the calling module.
    
    Returns:
        logging.Logger: Configured logger instance.
    """
    # Ensure we only set up the logger once
    if logging.getLogger(name).hasHandlers():
        return logging.getLogger(name)
    
    # Constants for logging setup
    LOG_DIR = "logs"
    LOG_FILENAME = os.path.join(LOG_DIR, "data_transformation_pipeline.log")
    LOG_LEVEL = logging.DEBUG
    FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    FILE_MAX_BYTES = 5 * 1024 * 1024  # 5 MB
    FILE_BACKUP_COUNT = 5

    # Create log directory if it doesn't exist
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(LOG_LEVEL)
    console_handler.setFormatter(FORMATTER)
    logger.addHandler(console_handler)

    # File handler with rotation
    file_handler = RotatingFileHandler(LOG_FILENAME, maxBytes=FILE_MAX_BYTES, backupCount=FILE_BACKUP_COUNT)
    file_handler.setLevel(LOG_LEVEL)
    file_handler.setFormatter(FORMATTER)
    logger.addHandler(file_handler)
    
    return logger

