from django.db import models


class Table(models.Model):
    capacity = models.PositiveIntegerField(verbose_name='вместимость')
    is_free = models.BooleanField(default=True, verbose_name='свободен')
    url = models.CharField(max_length=64, verbose_name='ссылка')


class TableInfo(models.Model):
    table_id = models.OneToOneField(Table, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=32, verbose_name='имя столика')
    info = models.TextField(verbose_name='описание столика')
    photo = models.ImageField(upload_to='restaurant/tables/')
