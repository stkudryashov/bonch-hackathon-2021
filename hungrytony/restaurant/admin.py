from django.contrib import admin
from restaurant.models import *


class TableInfoInLine(admin.TabularInline):
    model = TableInfo


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'capacity', 'is_free', 'url')
    list_display_links = ('id',)
    list_editable = ('is_free',)

    fieldsets = (
        ('Информация', {
            'fields': ('number', 'capacity', 'is_free')
        }),
        ('Ссылка', {
            'fields': ('url',)
        })
    )

    inlines = [
        TableInfoInLine
    ]


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


@admin.register(Settings)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('account_id', 'secret_key')
    list_display_links = ('account_id', 'secret_key')
