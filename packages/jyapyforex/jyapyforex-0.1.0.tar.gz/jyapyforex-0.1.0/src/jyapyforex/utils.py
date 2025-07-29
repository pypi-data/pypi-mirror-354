# This file contains reusable helper functions and common utilities for the library.

import logging
from datetime import datetime

# Configure a logger for the library's utility functions.
# This logger will propagate messages to the root logger, which can be configured by the user.
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler()) # Prevents "No handlers could be found for logger" warning

def validate_currency_code(currency: str) -> None:
    """
    Validates if the given string is a valid 3-letter alphabetic currency code.

    Args:
        currency (str): The currency code string to validate.

    Raises:
        ValueError: If the currency code is not a valid 3-letter alphabetic string.
    """
    if not (isinstance(currency, str) and len(currency) == 3 and currency.isalpha()):
        raise ValueError(f"Invalid currency code: '{currency}'. Must be a 3-letter alphabetic code (e.g., 'USD').")
    logger.debug(f"Currency code '{currency}' validated.")

def validate_date_format(date_str: str, date_format: str = "%Y-%m-%d") -> None:
    """
    Validates if the given string adheres to the specified date format.

    Args:
        date_str (str): The date string to validate.
        date_format (str): The expected format of the date string (default: "%Y-%m-%d").

    Raises:
        ValueError: If the date string does not match the expected format.
    """
    try:
        datetime.strptime(date_str, date_format)
        logger.debug(f"Date string '{date_str}' validated with format '{date_format}'.")
    except ValueError:
        raise ValueError(f"Invalid date format: '{date_str}'. Expected format: '{date_format}'.")
