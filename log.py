import functools
import logging
from logging.handlers import TimedRotatingFileHandler  # For daily rotation
from contextlib import redirect_stdout
from datetime import datetime

def log_function(func):
    """Decorator to log function execution, print statements, and validator errors.

    Args:
        func: The function to be decorated.

    Returns:
        The decorated function.
    """

    logger = logging.getLogger(func.__module__)  # Get logger for the current module

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Log function call and arguments
        logger.info(f"Calling function: {func.__name__}")
        logger.debug(f"Arguments: {args}, {kwargs}")

        # Capture print statements within the function
        def captured_print(*print_args, **print_kwargs):
            logger.info(f"Print inside {func.__name__}: {print_args[0]}")
                
        try:
            with redirect_stdout(captured_print):
                result = func(*args, **kwargs)
                logger.info(f"Result: {result}")
                return result
        except Exception as e:
            logger.exception(f"Error in {func.__name__}: {e}")
            raise
        # finally:
        #     print = original_print  # Restore original print function

    return wrapper
