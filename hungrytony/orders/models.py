from django.db import models
from restaurant.models import Table


class ProductCategory(models.Model):
    name = models.CharField(max_length=64, verbose_name='название')

    @property
    def get_products(self):
        return Product.objects.filter(categories__title=self.name)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Product(models.Model):
    name = models.CharField(max_length=64, verbose_name='название')
    info = models.TextField(verbose_name='описание блюда')
    cost = models.PositiveIntegerField(verbose_name='стоимость')
    photo = models.ImageField(upload_to='images/products/')

    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name='категория'
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'блюдо'
        verbose_name_plural = 'блюда'


class Order(models.Model):
    table_id = models.ForeignKey(Table, on_delete=models.PROTECT)
    order_id = models.CharField(max_length=64, verbose_name='идентификатор заказа')
    products = models.ManyToManyField(Product, through="ProductOrder", related_name='orders')

    def __str__(self):
        return f'{self.id}-{self.table_id.id}'

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'


class ProductOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f'{self.product}-{self.order}'

    class Meta:
        verbose_name = 'продукт-заказ'
        verbose_name_plural = 'продукты-заказы'
