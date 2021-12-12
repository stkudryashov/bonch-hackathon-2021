from django.contrib import admin
from telegrambot.models import *


@admin.register(TelegramUser)
class TelegramAdmin(admin.ModelAdmin):
    list_display = ('id', 'telegram_id')
