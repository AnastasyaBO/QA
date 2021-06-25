import requests
import json
from config import keys


class ConvertionException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):

        if quote == base:
            raise ConvertionException(f"Невозможно перевести одну и туже валюту ({base}).")
        try:
            quote_ticket = keys[quote]
        except KeyError:
            raise ConvertionException(f"Не удалось обработать валюту {quote}")

        try:
            base_ticket = keys[base]
        except KeyError:
            raise ConvertionException(f"Не удалось обработать валюту {base}")

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f"Не удалось обработать количество {amount}")

        quote_ticker = keys[quote]
        base_ticker = keys[base]
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]
        return total_base
