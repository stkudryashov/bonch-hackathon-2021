from django.contrib import admin
from orders.models import *


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')

    fieldsets = (
        ('Информация', {
            'fields': ('name',)
        }),
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'info', 'cost', 'category')
    list_display_links = ('name',)

    fieldsets = (
        ('Информация', {
            'fields': ('name', 'info', 'cost')
        }),
        ('Категория', {
            'fields': ('category',)
        }),
        ('Фотография', {
            'fields': ('photo',)
        })
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'table_id')
    list_display_links = ('id', 'table_id')

    fieldsets = (
        ('Информация', {
            'fields': ('table_id',)
        }),
        ('Заказ', {
            'fields': ('products',)
        })
    )
