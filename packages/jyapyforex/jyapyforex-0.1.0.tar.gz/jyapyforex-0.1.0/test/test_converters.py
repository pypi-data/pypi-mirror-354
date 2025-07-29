# test_script.py
from jyapyforex import ForexConverter
import time
import os

# Ensure your API key is set in your .env file before running this script
# For example: FIXER_IO_API_KEY=YOUR_ACTUAL_FIXER_IO_API_KEY

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def read_env_file(file_path):
    env_vars = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith('#'):  # Skip empty lines and comments
                    if '=' in line:
                        key, value = line.split('=', 1) # Split only at the first '='
                        env_vars[key] = value.strip()
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    return env_vars

if __name__ == '__main__':
    try:
        env_file_path = os.path.join(BASE_DIR, '.env')
        env_vars = read_env_file(env_file_path)
        for var, key in env_vars.items():
            api_keys = dict()
            api_keys[var] = key
            print(f"***** {var} ****")
            converter = ForexConverter(api_keys)

            date = "2023-01-15"
            from_currency = "USD"
            to_currency = "EUR"

            try:
                rate = converter.get_conversion_rate(from_currency, to_currency, date)
                print(f"1 {from_currency} = {rate:.4f} {to_currency} on {date}")
            except Exception as ex:
                print(f"An error occured while trying conversion rate using provider {var}. Error: {ex}")

            time.sleep(5)
            try:
                amount = 100.0
                converted_amount = converter.convert_amount(amount, from_currency, to_currency, date)
                print(f"{amount} {from_currency} = {converted_amount:.2f} {to_currency} on {date}")
            except Exception as ex:
                print(f"An error occured while trying amount conversion using provider {var}. Error: {ex}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")