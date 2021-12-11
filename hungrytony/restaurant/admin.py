from django.contrib import admin
from restaurant.models import *


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'capacity', 'is_free', 'url')
    list_display_links = ('id',)

    fieldsets = (
        ('Информация', {
            'fields': ('number', 'capacity', 'is_free')
        }),
        ('Ссылка', {
            'fields': ('url',)
        })
    )


@admin.register(TableInfo)
class TableInfoAdmin(admin.ModelAdmin):
    list_display = ('table_id', 'name', 'info')
    list_display_links = ('table_id', 'name')

    fieldsets = (
        ('Информация', {
            'fields': ('table_id', 'name', 'info')
        }),
        ('Фотография', {
            'fields': ('photo',)
        })
    )
