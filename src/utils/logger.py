import logging
import time
from functools import wraps


def get_logger(name):
    """
    Get a logger instance.
    Configuration is handled in the main entry point of the application.
    """
    return logging.getLogger(name)


def log_execution_time(func):
    """A decorator to log the execution time of a function."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)
        start_time = time.time()
        logger.info(f"Starting {func.__name__}...")
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        logger.info(f"Finished {func.__name__} in {elapsed_time:.4f} seconds.")
        return result

    return wrapper
