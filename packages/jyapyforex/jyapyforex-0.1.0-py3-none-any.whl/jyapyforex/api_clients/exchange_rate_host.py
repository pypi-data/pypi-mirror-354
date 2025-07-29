import requests
from datetime import datetime
from jyapyforex.exceptions import ForexAPIError, InvalidCurrencyError, RateNotFoundError, RateLimitExceededError
from jyapyforex.utils import logger

class ExchangeRateHostClient:
    """
    Client for interacting with the ExchangeRateHost API to retrieve forex rates.
    Requires an API key from ExchangeRateHost.
    """
    BASE_URL = "http://api.exchangerate.host/"

    def __init__(self, api_key: str):
        """
        Initializes the FixerIOClient with the provided API key.

        Args:
            api_key (str): Your API key for ExchangeRateHost.
        """
        if not api_key:
            logger.error("ExchangeRateHost API key cannot be empty.")
            raise ValueError("ExchangeRateHost API key cannot be empty.")
        self.api_key = api_key

    def get_historical_rate(self, date: str, base_currency: str, target_currency: str) -> float:
        """
        Fetches the historical exchange rate from ExchangeRateHost for a specific date.

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
        
        # ExchangeRateHost free plan typically uses USD as base
        default_base = 'USD'
        endpoint = f"{self.BASE_URL}historical?date={date}"
        params = {
            "date": date,
            "access_key": self.api_key,
            "currencies": f"{target_currency.upper()},{base_currency.upper()}"
        }
        logger.debug(f"Making API request to ExchangeRateHost: {endpoint} with params {params}")

        try:
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()
            logger.debug(f"ExchangeRateHost API response: {data}")

            if not data.get("success"):
                error_info = data.get("error", {})
                error_code = error_info.get('code')
                error_type = error_info.get('type', 'UnknownError')
                error_message = error_type
                detailed_error = f"ExchangeRateHost API Error ({error_type}, Code {error_code}): {error_message}"
                logger.error(detailed_error)

                if error_code == 101: # Invalid API Key
                    raise ForexAPIError(f"ExchangeRateHost API Error (Code {error_code}): Invalid API Key. {error_message}")
                elif error_code == 201: # Invalid base currency
                    raise InvalidCurrencyError(f"ExchangeRateHost API Error (Code {error_code}): Invalid base currency '{base_currency}'. {error_message}")
                elif error_code == 202: # Invalid symbols
                    raise InvalidCurrencyError(f"ExchangeRateHost API Error (Code {error_code}): Invalid target currency '{target_currency}'. {error_message}")
                elif error_code == 106: # Historical data not available for date
                    raise RateNotFoundError(f"ExchangeRateHost API Error (Code {error_code}): Historical data not available for date '{date}'. {error_message}")
                elif error_code == 104:
                    raise RateLimitExceededError(f"ExchangeRateHost API Error (Code {error_code}): Rate limit exceeded")
                else:
                    raise ForexAPIError(f"ExchangeRateHost API Error ({error_type}, Code {error_code}): {error_message}")

            rates = data.get("quotes", {})
            if default_base == base_currency.upper():
                return rates[default_base+target_currency.upper()]
            elif default_base+target_currency.upper() in rates and (default_base == base_currency.upper() or default_base+base_currency.upper() in rates):
                return rates[default_base+target_currency.upper()]/rates[default_base+base_currency.upper()]
            else:
                missing=""
                if default_base+target_currency.upper() not in rates:
                    missing = target_currency.upper()
                if default_base+base_currency.upper() not in rates:
                    if missing != "":
                        missing = missing + ", "
                    missing = missing + base_currency.upper()
                # This might happen if the API returns success but no rate for the specific symbol
                logger.warning(f"ExchangeRateHost did not return a rate for {missing} on {date}.")
                raise RateNotFoundError(f"Rate for {missing} not found for {date}.")

        except requests.exceptions.Timeout:
            raise ForexAPIError(f"ExchangeRateHost API request timed out after 10 seconds.")
        except requests.exceptions.ConnectionError:
            raise ForexAPIError(f"Could not connect to ExchangeRateHost API. Check your internet connection.")
        except requests.exceptions.RequestException as e:
            raise ForexAPIError(f"An unexpected request error occurred with ExchangeRateHost: {e}")
        except Exception as e:
            # Catch any other unexpected errors
            raise ForexAPIError(f"An unexpected error occurred while processing ExchangeRateHost response: {e}")
