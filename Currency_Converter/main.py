"""
Currency Converter using Fixer.io API.
Converts currency based on live exchange rates.

This version is refactored into a class-based structure to change the program flow.
"""

import requests
import sys
from pprint import pprint
class CurrencyConverter:
    """
    An object-oriented currency converter that encapsulates all related logic.
    """

    # === Constants moved into the class ===
    BASE_URL = "http://data.fixer.io/api/latest"
    STORAGE_FILE = "conversion_storage.txt"

    def __init__(self, api_key):
        """
        Initializes the converter, fetches rates, and prepares for operation.
        """
        self.api_key = api_key
        self.url = f"{self.BASE_URL}?access_key={self.api_key}"
        self.rates = self._get_exchange_rates()

    # === Core Logic Methods (Internal/Private) ===
    def _get_exchange_rates(self):
        """
        Fetches exchange rates from the Fixer.io API upon initialization.
        """
        try:
            response = requests.get(self.url)
            response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
            data = response.json()
            if data.get("success"):
                print("Successfully fetched exchange rates.")
                return data["rates"]
            else:
                print("API error:", data.get("error", {}).get("info", "Unknown API error"))
                sys.exit(1)
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch exchange rates: {e}")
            sys.exit(1)

    def _store_conversion(self, qty, from_currency, to_currency, amount):
        """
        Stores the result of a single conversion to the history file.
        """
        try:
            with open(self.STORAGE_FILE, "a") as file:
                file.write(f"{qty} {from_currency} = {amount} {to_currency}\n")
        except IOError as e:
            print(f"Error writing to history file: {e}")

    # === Public Methods for Application Features ===
    def display_history(self):
        """
        Displays all previous conversions from the storage file.
        """
        try:
            with open(self.STORAGE_FILE, "r") as file:
                history = file.read()
                if history:
                    print("\n--- Conversion History ---")
                    print(history.strip())
                else:
                    print("No conversion history found.")
        except FileNotFoundError:
            print("No conversion history found.")

    def display_currencies(self):
        """
        Displays all available currency codes in a formatted table.
        """
        print("\n--- Supported Currency Codes ---")
        currency_list = sorted(self.rates.keys())
        for i, code in enumerate(currency_list, 1):
            print(f"{code}", end="\t")
            if i % 8 == 0:
                print()
        print("\n")

    def convert_currency(self, qty, from_currency, to_currency):
        """
        Performs the currency conversion calculation.
        """
        try:
            from_rate = self.rates[from_currency]
            to_rate = self.rates[to_currency]
            converted_amount = round((float(qty) / from_rate) * to_rate, 2)
            return converted_amount
        except KeyError as e:
            print(f"Invalid currency code: {e}. Please check and try again.")
            return None
        except ValueError:
            print("Invalid amount. Please enter a number.")
            return None

    def run(self):
        """
        The main user interface loop to run the application.
        """
        if not self.rates:
            print("Cannot start converter due to rate fetching error.")
            return

        print("Currency Converter Ready.\n")
        while True:
            query = input(
                "\nEnter: <amount> <from_currency> <to_currency>\n"
                "Type 'C' to view currencies, 'H' for history, or 'Q' to quit: "
            ).strip().upper()

            if query == "Q":
                print("Exiting... Goodbye!")
                break
            elif query == "C":
                self.display_currencies()
            elif query == "H":
                self.display_history()
            else:
                try:
                    qty_str, from_curr, to_curr = query.split()
                    qty = float(qty_str)
                    result = self.convert_currency(qty, from_curr, to_curr)
                    if result is not None:
                        print(f"-> {qty} {from_curr} = {result} {to_curr}")
                        self._store_conversion(qty, from_curr, to_curr, result)
                except ValueError:
                    print("Invalid input format. Use: <amount> <from_currency> <to_currency>")
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")


# === Run ===
if __name__ == "__main__":
    API_KEY = "33ec7c73f8a4eb6b9b5b5f95118b2275" # Replace with your actual key
    converter = CurrencyConverter(api_key=API_KEY)
    converter.run()