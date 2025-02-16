import requests
from django.apps import AppConfig


class PriceNotificationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "price_notifications"

    def ready(self):
        # XAUUSD real-time price is displayed in '/price_notification/' page
        requests.patch(
            'http://metatrader5_api_service:8080/symbol_exists/XAUUSD'
        )
