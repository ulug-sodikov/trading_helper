from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Notification(models.Model):
    class PriceType(models.TextChoices):
        BID_PRICE = "BID_PRICE",
        ASK_PRICE = "ASK_PRICE"

    class ComparisonType(models.TextChoices):
        GREATER_THAN = "GREATER_THAN"
        LESS_THAN = "LESS_THAN"

    symbol = models.CharField(max_length=20)
    target_price = models.DecimalField(max_digits=50, decimal_places=30)
    comparison_type = models.CharField(max_length=12, choices=ComparisonType)
    tracking_price_type = models.CharField(max_length=9, choices=PriceType)
    created_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return (
            f'IF {self.symbol} {self.tracking_price_type} {self.comparison_type} '
            f'{self.target_price}, NOTIFY {self.user.username}'
        )

    @classmethod
    def get_triggered_notifications(cls, symbol, bid, ask):
        """
        Returns a list of triggered notifications for the given symbol
        and ticks.

        Four possible scenarios can be specified for notification
        to trigger:
        - If bid price is greater than target price, and tracking price is bid price.
        - If bid price is less than target price, and tracking price is bid price.
        - If ask price is greater than target price, and tracking price is ask price.
        - If ask price is less than target, and tracking price is ask price.
        """
        query = models.Q(
            tracking_price_type=cls.PriceType.BID_PRICE,
            comparison_type=cls.ComparisonType.GREATER_THAN,
            target_price__lt=bid
        )
        query |= models.Q(
            tracking_price_type=cls.PriceType.BID_PRICE,
            comparison_type=cls.ComparisonType.LESS_THAN,
            target_price__gt=bid
        )
        query |= models.Q(
            tracking_price_type=cls.PriceType.ASK_PRICE,
            comparison_type=cls.ComparisonType.GREATER_THAN,
            target_price__lt=ask
        )
        query |= models.Q(
            tracking_price_type=cls.PriceType.ASK_PRICE,
            comparison_type=cls.ComparisonType.LESS_THAN,
            target_price__gt=ask
        )

        return cls.objects.filter(query, symbol=symbol)
