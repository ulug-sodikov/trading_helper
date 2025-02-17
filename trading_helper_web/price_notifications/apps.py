import threading

import requests
from django.apps import AppConfig

from .price_polling_loop import start_price_polling_loop


class PriceNotificationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "price_notifications"

    def ready(self):
        # XAUUSD real-time price is displayed in '/price_notification/' page
        requests.patch(
            'http://metatrader5_api_service:8080/symbol_exists/XAUUSD'
        )

        # Since PriceNotificationsConfig.ready method might be executed twice,
        # price-polling-loop thread existence should be checked before creating
        # it, otherwise two threads can be created
        for _thread in threading.enumerate():
            if _thread.name == 'price-polling-loop':
                break
        else:
            new_thread = threading.Thread(
                target=start_price_polling_loop, name='price-polling-loop'
            )
            new_thread.start()
