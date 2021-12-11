from django.db import models


class Table(models.Model):
    number = models.CharField(max_length=32, verbose_name='номер столика')
    capacity = models.PositiveIntegerField(verbose_name='вместимость')
    is_free = models.BooleanField(default=True, verbose_name='свободен')
    url = models.CharField(max_length=64, verbose_name='ссылка')

    def __str__(self):
        return f'Столик №{self.number}'

    class Meta:
        verbose_name = 'столик'
        verbose_name_plural = 'столики'


class TableInfo(models.Model):
    table_id = models.OneToOneField(Table, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=32, verbose_name='имя столика')
    info = models.TextField(verbose_name='описание столика')
    photo = models.ImageField(upload_to='images/tables/')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'информация о столике'
        verbose_name_plural = 'информация о столиках'
