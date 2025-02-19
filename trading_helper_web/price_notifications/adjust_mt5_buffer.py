import requests

from .models import Notification


def adjust_mt5_buffer():
    symbols = {row['symbol'] for row in Notification.objects.values('symbol')}
    response = requests.get(
        'http://metatrader5_api_service:8080/symbols_buffer'
    )
    mt5_symbols_buffer = set(response.json()['symbols_buffer'])

    for symbol in symbols.difference(mt5_symbols_buffer):
        requests.patch(
            f'http://metatrader5_api_service:8080/symbols_buffer/{symbol}'
        )

    # Symbols that are not present in database but present in mt5 symbols_buffer
    ghost_symbols = mt5_symbols_buffer.difference(symbols)
    # XAUUSD ticks are used in frontend, thus XAUUSD shoud not be removed
    # from mt5 symbols_buffer
    ghost_symbols.discard('XAUUSD')
    for symbol in ghost_symbols:
        requests.delete(
            f'http://metatrader5_api_service:8080/symbols_buffer/{symbol}'
        )
