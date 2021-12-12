import uuid

from django.core.management.base import BaseCommand
from django.conf import settings

from telegram import Bot, Update

from telegram.ext import Updater, CommandHandler
from telegram.ext import CallbackContext, CallbackQueryHandler

from telegram.utils.request import Request

from datetime import datetime
from datetime import timedelta

import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

from orders.models import Order
from restaurant.models import Settings, Table
from telegrambot.models import TelegramUser

time_delta = timedelta(minutes=5)


def get_or_create_profile(f):
    def inner(update=None, telegram_id=None):
        try:
            chat_id = update.message.chat_id
            p, _ = TelegramUser.objects.get_or_create(
                telegram_id=chat_id,
            )
            f(p.telegram_id)
        except AttributeError:
            f(update)
    return inner


def back_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text='🔙  Назад', callback_data='BackMenu')]])


def edit_messages(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data

    button_press = data
    edit_message = (query.message.chat_id, query.message.message_id)

    user = TelegramUser.objects.get(telegram_id=query.message.chat_id)

    telegram_token = Settings.objects.first().telegram_token
    bot = telepot.Bot(telegram_token)

    if 'BackMenu' in button_press:
        try:
            bot.deleteMessage(edit_message)
        except telepot.exception.TelegramError:
            pass
        finally:
            messages(user.telegram_id)
    elif 'ReserveTable' in button_press:
        try:
            bot.deleteMessage(edit_message)
        except telepot.exception.TelegramError:
            pass
        finally:
            table_view(user.telegram_id)
    elif 'OrderOnRoad' in button_press:
        try:
            bot.deleteMessage(edit_message)
        except telepot.exception.TelegramError:
            pass
        finally:
            bot.sendMessage(user.telegram_id, text='2', reply_markup=back_keyboard())
    elif 'DoReserve' in button_press:
        try:
            bot.deleteMessage(edit_message)
        except telepot.exception.TelegramError:
            pass
        finally:
            value = button_press.split()[1]
            create_order(user.telegram_id, value)


@get_or_create_profile
def messages(telegram_id):
    telegram_token = Settings.objects.first().telegram_token
    bot = telepot.Bot(telegram_token)

    user = TelegramUser.objects.get(telegram_id=telegram_id)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text='Забронировать  🎉', callback_data='ReserveTable'),
                          InlineKeyboardButton(text='Заказать с собой 🥳', callback_data='OrderOnRoad')]]
    )

    bot.sendMessage(chat_id=user.telegram_id, text='Добро пожаловать!', reply_markup=keyboard)


def table_view(telegram_id):
    telegram_token = Settings.objects.first().telegram_token
    bot = telepot.Bot(telegram_token)

    user = TelegramUser.objects.get(telegram_id=telegram_id)

    tables = Table.objects.all()
    bot.sendMessage(chat_id=user.telegram_id, text='Выберите свой столик 🎉', reply_markup=back_keyboard())

    for table in tables:
        message = f'{table.tableinfo.name}\n\n{table.tableinfo.info}'

        if table.is_free:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text='Забронировать  🎉', callback_data=f'DoReserve {table.id}')]]
            )
        else:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[[]]
            )

            message += '\n\n*сейчас столик занят*'

        bot.sendPhoto(chat_id=user.telegram_id, photo=table.tableinfo.photo,
                      caption=message, reply_markup=keyboard)


def create_order(telegram_id, table_id):
    telegram_token = Settings.objects.first().telegram_token
    bot = telepot.Bot(telegram_token)

    user = TelegramUser.objects.get(telegram_id=telegram_id)

    table = Table.objects.get(id=table_id)

    table.is_free = False

    secret_uuid = uuid.uuid4()

    table.url = secret_uuid
    table.save()

    order = Order.objects.create(table_id=table, order_id=secret_uuid)

    bot.sendMessage(chat_id=user.telegram_id, text=f'{order.order_id}')


class Command(BaseCommand):
    help = 'Hungry Tony'

    def handle(self, *args, **options):
        request = Request(connect_timeout=0.5, read_timeout=1.0)
        telegram_token = Settings.objects.first().telegram_token
        bot = Bot(request=request, token=telegram_token)

        updater = Updater(bot=bot)

        case_handler = CommandHandler('start', messages)
        updater.dispatcher.add_handler(case_handler)

        buttons_handler = CallbackQueryHandler(callback=edit_messages, pass_chat_data=False)
        updater.dispatcher.add_handler(buttons_handler)

        updater.start_polling()
        updater.idle()
