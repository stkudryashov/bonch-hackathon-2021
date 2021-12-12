from django.db import models

from orders.models import Order


class TelegramUser(models.Model):
    telegram_id = models.CharField(max_length=32)
    order_id = models.CharField(max_length=64, blank=True, null=True)
