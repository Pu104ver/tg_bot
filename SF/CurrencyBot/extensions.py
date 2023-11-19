import json
import requests
from cfg import CURRENCIES


class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(base, quote, amount):
        try:
            amount = float(amount)
            if amount <= 0:
                raise APIException('Некорректное значение количества')

            if base not in CURRENCIES or quote not in CURRENCIES:
                raise APIException('Некорректные валюты')

        except ValueError:
            raise APIException('Некорректное значение количества')

        if base == quote:
            raise APIException('Конвертация одной валюты недоступна')

        try:
            r = requests.get(
                f'https://min-api.cryptocompare.com/data/price?fsym={CURRENCIES[base]}&tsyms={CURRENCIES[quote]}')

            response = (f'{amount} {CURRENCIES[base]} = '
                        f'{round(json.loads(r.content)[CURRENCIES[quote]] * amount, 5)} {CURRENCIES[quote]}')
            return response
        except requests.RequestException as e:
            raise APIException(f'Ошибка при получении данных: {e}')
        except json.JSONDecodeError as e:
            raise APIException(f'Ошибка при декодировании JSON: {e}')
