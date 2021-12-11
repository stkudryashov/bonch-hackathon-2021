from django.db import models

# Create your models here.
from orders.models import Product, Order
from restaurant.models import Table


class TableVk(models.Model):
    table = models.OneToOneField(Table, on_delete=models.CASCADE, verbose_name="столик", null=False)
    vk_photo_id = models.TextField(verbose_name='id фотографии', blank=True, null=True)

    def __str__(self):
        return str(self.table)

    class Meta:
        verbose_name = 'столик ВК'
        verbose_name_plural = 'столики ВК'


class ProductVk(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, verbose_name="продукт", null=False)
    vk_photo_id = models.TextField(verbose_name="id фотографии", blank=True, null=True)

    def __str__(self):
        return str(self.product)

    class Meta:
        verbose_name = 'продукт ВК'
        verbose_name_plural = 'продукты ВК'


class ClientVK(models.Model):
    user_id = models.IntegerField(verbose_name="id пользователя", null=False)
    order = models.OneToOneField(Order, verbose_name="заказ", null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user_id}"

    class Meta:
        verbose_name = 'заказ ВК'
        verbose_name_plural = 'заказы ВК'
