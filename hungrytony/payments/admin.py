from django.contrib import admin
from payments.models import Payment


@admin.register(Payment)
class YandexPaymentAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'table_id', 'payment_id', 'status', 'cost', 'info', 'is_closed', 'datetime')
    list_display_links = ('order_id', 'table_id', 'payment_id')

    fieldsets = (
        ('Информация', {
            'fields': ('order_id', 'table_id')
        }),
        ('Платеж', {
            'fields': ('payment_id', 'status', 'cost')
        }),
        ('Другое', {
            'fields': ('info', 'is_closed')
        })
    )
