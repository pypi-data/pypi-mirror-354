# Custom exception classes for better error handling in the library.

class ForexAPIError(Exception):
    """Base exception for errors related to forex API interactions."""
    pass

class InvalidCurrencyError(ForexAPIError):
    """Raised when an invalid currency code is provided."""
    pass

class RateNotFoundError(ForexAPIError):
    """Raised when a conversion rate cannot be found for the given parameters."""
    pass

class RateLimitExceededError(ForexAPIError):
    """Raised when rate limit is exceeded for the given parameters."""
    pass