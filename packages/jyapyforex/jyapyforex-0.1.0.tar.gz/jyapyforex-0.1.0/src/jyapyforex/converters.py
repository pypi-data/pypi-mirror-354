# This is the main public interface for the library.
# It orchestrates calls to different API clients and provides conversion functionality.
 
import os
from datetime import datetime
from typing import Dict, Optional

# Import specific API clients
from jyapyforex.api_clients.fixer_io import FixerIOClient
from jyapyforex.api_clients.open_exchange_rates import OpenExchangeRatesClient
from jyapyforex.api_clients.exchange_rate_host import ExchangeRateHostClient

# from jyapyforex.api_clients.oanda import OandaClient # Future client

from jyapyforex.exceptions import ForexAPIError, InvalidCurrencyError, RateNotFoundError

class ForexConverter:
    """
    A unified converter for fetching and converting foreign exchange rates
    from various API providers.
    """
    def __init__(self, api_keys: Optional[Dict[str, str]] = None):
        """
        Initializes the ForexConverter.

        API keys can be provided either via the `api_keys` dictionary
        or as environment variables. Environment variables are preferred for security.

        Args:
            api_keys (Optional[Dict[str, str]]): A dictionary of API keys,
                                                 e.g., {'FIXER_IO_API_KEY': 'your_key'}.
                                                 If None, environment variables are checked.

        Raises:
            ValueError: If no valid API keys are provided or found for any configured provider.
        """
        self.api_clients = {}
        self._load_api_clients(api_keys)

    def _load_api_clients(self, api_keys):
        """
        Loads and initializes API clients based on provided API keys or environment variables.
        """
        # Prioritize API keys passed directly, then environment variables
        # For security, strongly recommend environment variables or a secrets manager in production.
        # For a library, it's common to accept keys via constructor or environment variables.

        # Fixer.io
        fixer_api_key = (api_keys.get('FIXER_IO_API_KEY') if api_keys else None) or os.getenv('FIXER_IO_API_KEY')
        if fixer_api_key:
            self.api_clients['fixer_io'] = FixerIOClient(fixer_api_key)

        # OpenExchangeRatesClient
        open_exchange_rates_key = (api_keys.get('OPEN_EXCHANGE_RATES_API_KEY') if api_keys else None) or os.getenv('OPEN_EXCHANGE_RATES_API_KEY')
        if open_exchange_rates_key:
            self.api_clients['open_exchange_rates'] = OpenExchangeRatesClient(open_exchange_rates_key)
        
        # ExchangeRateHostClient
        exchange_rate_host_key = (api_keys.get('EXCHANGE_RATE_HOST_API_KEY') if api_keys else None) or os.getenv('EXCHANGE_RATE_HOST_API_KEY')
        if exchange_rate_host_key:
            self.api_clients['exchange_rate_host'] = ExchangeRateHostClient(exchange_rate_host_key)
        
        # Add other API clients here (e.g., OpenExchangeRatesClient, OandaClient)
        # open_exchange_rates_key = (api_keys.get('OPEN_EXCHANGE_RATES_API_KEY') if api_keys else None) or os.getenv('OPEN_EXCHANGE_RATES_API_KEY')
        # if open_exchange_rates_key:
        #     self.api_clients['open_exchange_rates'] = OpenExchangeRatesClient(open_exchange_rates_key)

        if not self.api_clients:
            raise ValueError(
                "No valid API keys provided or found in environment variables "
                "for any supported forex provider (e.g., FIXER_IO_API_KEY). "
                " Please set API keys for at least one provider."
            )

    def get_conversion_rate(self, from_currency: str, to_currency: str, date: str) -> float:
        """
        Gets the conversion rate between two currencies for a given date.
        It attempts to retrieve the rate from available API providers in order.

        Args:
            from_currency (str): The three-letter currency code for the source currency (e.g., "USD").
            to_currency (str): The three-letter currency code for the target currency (e.g., "EUR").
            date (str): The date for which to retrieve the rate, in "YYYY-MM-DD" format.

        Returns:
            float: The conversion rate from `from_currency` to `to_currency` on `date`.

        Raises:
            ValueError: If the date format is incorrect.
            InvalidCurrencyError: If provided currency codes are invalid.
            RateNotFoundError: If the rate cannot be found from any configured provider for the given date.
            ForexAPIError: For other API-related issues.
        """
        # Validate date format (e.g., using datetime.strptime)
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date format. Please use YYYY-MM-DD.")
        
        # Ensure currency codes are valid (e.g., 3 uppercase letters)
        if not (isinstance(from_currency, str) and len(from_currency) == 3 and from_currency.isalpha()):
            raise InvalidCurrencyError(f"Invalid 'from_currency' code: '{from_currency}'. Must be a 3-letter alphabetic code.")
        if not (isinstance(to_currency, str) and len(to_currency) == 3 and to_currency.isalpha()):
            raise InvalidCurrencyError(f"Invalid 'to_currency' code: '{to_currency}'. Must be a 3-letter alphabetic code.")

        if from_currency == to_currency:
            return 1.0
        # Iterate through available API clients and try to get the rate
        for provider_name, client in self.api_clients.items():
            try:
                rate = client.get_historical_rate(date, from_currency, to_currency)
                print(f"Rate obtained from {provider_name}") # For debugging/logging
                return rate
            except Exception as e:
                print(f"Failed to get rate from {provider_name}: {e}")
                continue
        raise RateNotFoundError(
            f"Could not retrieve conversion rate for {from_currency.upper()} to {to_currency.upper()} "
            f"on {date} from any configured API provider."
        )

    def convert_amount(self, amount: float, from_currency: str, to_currency: str, date: str) -> float:
        """
        Converts a given amount from one currency to another for a specific date.

        Args:
            amount (float): The amount to convert.
            from_currency (str): The three-letter currency code for the source currency.
            to_currency (str): The three-letter currency code for the target currency.
            date (str): The date for which to use the exchange rate, in "YYYY-MM-DD" format.

        Returns:
            float: The converted amount.

        Raises:
            ValueError: If the date format is incorrect.
            InvalidCurrencyError: If provided currency codes are invalid.
            RateNotFoundError: If the rate cannot be found from any configured provider for the given date.
            ForexAPIError: For other API-related issues.
        """
        if not isinstance(amount, (int, float)):
            raise ValueError("Amount must be a number.")
        if amount < 0:
            raise ValueError("Amount cannot be negative.")
        rate = self.get_conversion_rate(from_currency, to_currency, date)
        return amount * rate