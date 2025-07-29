import requests
from datetime import datetime
from jyapyforex.exceptions import ForexAPIError, InvalidCurrencyError, RateNotFoundError, RateLimitExceededError
from jyapyforex.utils import logger

class FixerIOClient:
    """
    Client for interacting with the Fixer.io API to retrieve forex rates.
    Requires an API key from Fixer.io.
    """
    BASE_URL = "http://data.fixer.io/api/"

    def __init__(self, api_key: str):
        """
        Initializes the FixerIOClient with the provided API key.

        Args:
            api_key (str): Your API key for Fixer.io.
        """
        if not api_key:
            logger.error("Fixer.io API key cannot be empty.")
            raise ValueError("Fixer.io API key cannot be empty.")
        self.api_key = api_key

    def get_historical_rate(self, date: str, base_currency: str, target_currency: str, retry: bool=False) -> float:
        """
        Fetches the historical exchange rate from Fixer.io for a specific date.

        Args:
            date (str): The date for which to retrieve the rate, in "YYYY-MM-DD" format.
            base_currency (str): The three-letter currency code for the base currency (e.g., "USD").
            target_currency (str): The three-letter currency code for the target currency (e.g., "EUR").

        Returns:
            float: The conversion rate from base_currency to target_currency on the given date.

        Raises:
            ValueError: If the date format is incorrect or currency codes are invalid.
            ForexAPIError: If there's an issue with the API request or response.
            RateNotFoundError: If the rate for the specified currencies/date is not available.
        """
        # Validate date format
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            logger.error(f"Invalid date format: '{date}'. Expected YYYY-MM-DD.")
            raise ValueError(f"Invalid date format: '{date}'. Expected YYYY-MM-DD.")
        
        # Fixer.io free plan typically uses EUR as base
        default_base = 'EUR'
        endpoint = f"{self.BASE_URL}{date}"
        params = {
            "access_key": self.api_key,
            "base": default_base.upper(), # Ensure currency codes are uppercase
            "symbols": f"{target_currency.upper()},{base_currency.upper()}"
        }
        logger.debug(f"Making API request to Fixer.io: {endpoint} with params {params}")

        try:
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()
            logger.debug(f"Fixer.io API response: {data}")

            if not data.get("success"):
                error_info = data.get("error", {})
                error_code = error_info.get('code')
                error_type = error_info.get('type', 'UnknownError')
                error_message = error_info.get('info', 'No specific error information provided.')
                detailed_error = f"Fixer.io API Error ({error_type}, Code {error_code}): {error_message}"
                logger.error(detailed_error)
                
                if error_code == 101: # Invalid API Key
                    raise ForexAPIError(f"Fixer.io API Error (Code {error_code}): Invalid API Key. {error_message}")
                elif error_code == 201: # Invalid base currency
                    raise InvalidCurrencyError(f"Fixer.io API Error (Code {error_code}): Invalid base currency '{base_currency}'. {error_message}")
                elif error_code == 202: # Invalid symbols
                    raise InvalidCurrencyError(f"Fixer.io API Error (Code {error_code}): Invalid target currency '{target_currency}'. {error_message}")
                elif error_code == 302: # Historical data not available for date
                    raise RateNotFoundError(f"Fixer.io API Error (Code {error_code}): Historical data not available for date '{date}'. {error_message}")
                elif error_code == 106:
                    raise RateLimitExceededError(f"Fixer.io API Error (Code {error_code}): Rate limit exceeded")
                else:
                    raise ForexAPIError(f"Fixer.io API Error ({error_type}, Code {error_code}): {error_message}")

            rates = data.get("rates", {})
            if target_currency.upper() in rates and base_currency.upper() in rates:
                return rates[target_currency.upper()]/rates[base_currency.upper()]
            else:
                missing=""
                if target_currency.upper() not in rates:
                    missing = target_currency.upper()
                if base_currency.upper() not in rates:
                    if missing != "":
                        missing = missing + ", "
                    missing = missing + base_currency.upper()
                # This might happen if the API returns success but no rate for the specific symbol
                logger.warning(f"Fixer.io did not return a rate for {missing} on {date}.")
                raise RateNotFoundError(f"Rate for {missing} not found for {date}.")

        except requests.exceptions.Timeout:
            raise ForexAPIError(f"Fixer.io API request timed out after 10 seconds.")
        except requests.exceptions.ConnectionError:
            raise ForexAPIError(f"Could not connect to Fixer.io API. Check your internet connection.")
        except requests.exceptions.RequestException as e:
            raise ForexAPIError(f"An unexpected request error occurred with Fixer.io: {e}")
        except Exception as e:
            # Catch any other unexpected errors
            raise ForexAPIError(f"An unexpected error occurred while processing Fixer.io response: {e}")
