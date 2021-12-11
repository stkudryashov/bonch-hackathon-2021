from django.db import models
from restaurant.models import Table


class Payment(models.Model):
    order_id = models.CharField(max_length=64)
    table_id = models.ForeignKey(Table, on_delete=models.PROTECT)

    payment_id = models.CharField(max_length=64, blank=True, null=True)
    status = models.CharField(max_length=64, blank=True, null=True)

    cost = models.PositiveIntegerField()
    info = models.TextField(blank=True, null=True)

    is_closed = models.BooleanField(default=False)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.order_id}'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'список платежей'
