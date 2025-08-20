"""
Logging configuration utilities
"""

import logging
import sys
from pathlib import Path
from typing import Optional

def setup_logging(
    level: str = "INFO",
    log_file: Optional[str] = None,
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
) -> logging.Logger:
    """Setup logging configuration"""
    
    # Convert string level to logging level
    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {level}")
    
    # Create logger
    logger = logging.getLogger("jeffs_api_ripper")
    logger.setLevel(numeric_level)
    
    # Remove existing handlers to avoid duplicates
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(numeric_level)
    
    # Create formatter
    formatter = logging.Formatter(log_format)
    console_handler.setFormatter(formatter)
    
    # Add console handler to logger
    logger.addHandler(console_handler)
    
    # Create file handler if log_file is specified
    if log_file:
        try:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(numeric_level)
            file_handler.setFormatter(formatter)
            
            logger.addHandler(file_handler)
            logger.info(f"Logging to file: {log_file}")
            
        except Exception as e:
            logger.warning(f"Failed to setup file logging: {str(e)}")
    
    # Set logging level for other modules
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("selenium").setLevel(logging.WARNING)
    
    logger.info(f"Logging initialized with level: {level}")
    return logger

def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the specified name"""
    return logging.getLogger(f"jeffs_api_ripper.{name}")
