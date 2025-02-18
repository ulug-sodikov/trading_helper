import json
from decimal import Decimal

from .utils.immortal_ws import ImmortalWebSocket


def start_price_polling_loop():
    from .models import Notification

    from .adjust_mt5_buffer import adjust_mt5_buffer
    adjust_mt5_buffer()

    ws = ImmortalWebSocket()
    ws.connect('ws://metatrader5_api_service:8080/')

    while True:
        response = ws.recv()
        try:
            data = json.loads(response)
        except (json.JSONDecodeError, TypeError):
            data = None

        if data is not None:
            for notification in Notification.get_triggered_notifications(
                    symbol=data['symbol'],
                    bid=Decimal(str(data['bid'])),
                    ask=Decimal(str(data['ask']))
            ):
                # Notify telegram users.
                notification.delete()
