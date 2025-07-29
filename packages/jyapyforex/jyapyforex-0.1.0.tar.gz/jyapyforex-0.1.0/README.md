# Just Yet Another library for forex conversions

A Python library for fetching historical foreign exchange (forex) rates from various popular providers. This library aims to simplify currency conversion for a given date by abstracting away the complexities of different API integrations.

## Features

* **Unified Interface:** Get conversion rates using a single, consistent API.
* **Multiple Provider Support:** Designed to support multiple forex API providers (currently includes Fixer.io, ExchangeRateHost, OpenExchangeRates).
* **Historical Data:** Fetch rates for specific past dates.
* **Secure API Key Handling:** Utilizes environment variables for API key management.

## Installation

You can install `jyapyforex` using pip:

```bash
pip install jyapyforex
```

## API Keys

This library requires API keys from the forex rate providers you wish to use. For security, it's highly recommended to store your API keys as environment variables.

**Example for Fixer.io:**

1.  Sign up for an API key at [Fixer.io](https://fixer.io/).
2.  Set your API key as an environment variable:

    * **Linux/macOS:**
        ```bash
        export FIXER_IO_API_KEY="your_fixer_io_api_key_here"
        ```
        (Add this line to your `~/.bashrc`, `~/.zshrc`, or equivalent for persistence)

    * **Windows (Command Prompt):**
        ```cmd
        set FIXER_IO_API_KEY="your_fixer_io_api_key_here"
        ```
        (For persistence, you'll need to set it via System Properties -> Environment Variables)

    * **Windows (PowerShell):**
        ```powershell
        $env:FIXER_IO_API_KEY="your_fixer_io_api_key_here"
        ```
        (For persistence, you'll need to set it in your PowerShell profile)

Alternatively, you can pass the API keys directly to the `ForexConverter` constructor as a dictionary.

Following are the expected environment variables for supported providers:
|     Provider         |            Key              |
| -------------------- | --------------------------- |
| Fixer.io             | FIXER_IO_API_KEY            |
| Open Exchange Rates  | OPEN_EXCHANGE_RATES_API_KEY |
| Exchange Rate Host   | EXCHANGE_RATE_HOST_API_KEY  |

## Usage

Here's how to use the `ForexConverter` to get historical exchange rates:

```python
from jyapyforex import ForexConverter

# Initialize the converter. It will automatically look for API keys
# in environment variables or you can pass them explicitly.
try:
    converter = ForexConverter()

    # Example 1: Get the conversion rate from USD to EUR on a specific date
    date = "2023-01-15"
    from_currency = "USD"
    to_currency = "EUR"

    rate = converter.get_conversion_rate(from_currency, to_currency, date)
    print(f"1 {from_currency} = {rate:.4f} {to_currency} on {date}")

    # Example 2: Convert an amount
    amount = 100.0
    converted_amount = converter.convert_amount(amount, from_currency, to_currency, date)
    print(f"{amount} {from_currency} = {converted_amount:.2f} {to_currency} on {date}")

    # Example 3: If you want to pass API keys directly (less secure for production)
    # api_keys = {
    #     "FIXER_IO_API_KEY": "your_api_key_here_if_not_using_env_vars"
    # }
    # converter_with_keys = ForexConverter(api_keys=api_keys)
    # rate_direct = converter_with_keys.get_conversion_rate("GBP", "JPY", "2024-05-20")
    # print(f"1 GBP = {rate_direct:.4f} JPY on 2024-05-20 (using direct keys)")

except ValueError as e:
    print(f"Configuration Error: {e}")
except Exception as e:
    print(f"An error occurred: {e}")

```
### Command-Line Interface (CLI)

After installation, you can use the `jyapyforex` command directly from your terminal:

* **Get a conversion rate:**
    ```bash
    jyapyforex rate USD EUR 2023-01-15
    ```
* **Convert an amount:**
    ```bash
    jyapyforex convert 100 USD EUR 2023-01-15
    ```
* **Get help:**
    ```bash
    jyapyforex --help
    jyapyforex rate --help
    ```
* **Enable debug logging:**
    ```bash
    jyapyforex --debug rate USD EUR 2023-01-15
    ```

## Supported Currencies

The supported currencies depend on the integrated API providers. Generally, popular currencies like USD, EUR, GBP, JPY, CAD, AUD, CHF, etc., are widely supported. Refer to the documentation of each specific API provider (e.g., Fixer.io) for a complete list.

## Adding More API Providers

To add support for a new API provider:

1.  Create a new Python file in `src/jyapyforex/api_clients/` (e.g., `open_exchange_rates.py`).
2.  Implement a class for the new API client (e.g., `OpenExchangeRatesClient`) with a `get_historical_rate` method that matches the signature of `FixerIOClient`.
3.  Import and instantiate your new client in `src/jyapyforex/converters.py` within the `_load_api_clients` method, checking for its corresponding environment variable or passed API key.

## Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests on the [GitHub repository](https://github.com/JustYetAnother/jyapyforex).

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.