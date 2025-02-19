import json
from decimal import Decimal

import requests

from .utils.immortal_ws import ImmortalWebSocket


def create_request_json(notification):
    return {
        'tg_user_id': notification.user.username,
        'text': (
            f'{notification.symbol} {notification.tracking_price_type} '
            f'hits {notification.target_price.normalize()}'
        ),
        'notification_id': notification.id,
        'timestamp': int(notification.created_at.timestamp()),
    }


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
                requests.post(
                    'http://tg_bot_notifications_api_service:8040/notify',
                    json=create_request_json(notification)
                )
                notification.delete()
