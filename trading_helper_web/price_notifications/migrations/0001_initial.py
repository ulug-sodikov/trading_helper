# Generated by Django 5.1 on 2025-02-12 08:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Notification",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("symbol", models.CharField(max_length=20)),
                ("target_price", models.DecimalField(decimal_places=30, max_digits=50)),
                (
                    "comparison_type",
                    models.CharField(
                        choices=[
                            ("GREATER_THAN", "Greater Than"),
                            ("LESS_THAN", "Less Than"),
                        ],
                        max_length=12,
                    ),
                ),
                (
                    "tracking_price_type",
                    models.CharField(
                        choices=[
                            ("BID_PRICE", "Bid Price"),
                            ("ASK_PRICE", "Ask Price"),
                        ],
                        max_length=9,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
