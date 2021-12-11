from django.contrib import admin
from vkbot.models import *


@admin.register(TableVk)
class TableVkAdmin(admin.ModelAdmin):
    list_display = ('id', 'table', "vk_photo_id")


@admin.register(ProductVk)
class OrderVkAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', "vk_photo_id")


@admin.register(ClientVK)
class ClientVkAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', "order")
