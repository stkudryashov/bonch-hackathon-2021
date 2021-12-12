import uuid

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db.models import Sum

from payments.models import Payment as ModelPayment

from telegram import Bot, Update

from telegram.ext import Updater, CommandHandler
from telegram.ext import CallbackContext, CallbackQueryHandler

from telegram.utils.request import Request

from datetime import datetime
from datetime import timedelta

import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from yookassa import Configuration, Payment

from orders.models import Order, ProductCategory, Product, ProductOrder
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
            bot.sendMessage(user.telegram_id, text='Пока недоступно 🥲 ', reply_markup=back_keyboard())
    elif 'DoReserve' in button_press:
        try:
            bot.deleteMessage(edit_message)
        except telepot.exception.TelegramError:
            pass
        finally:
            value = button_press.split()[1]
            create_order(user.telegram_id, value)
    elif 'ViewCategory' in button_press:
        try:
            bot.deleteMessage(edit_message)
        except telepot.exception.TelegramError:
            pass
        finally:
            value = button_press.split()[1]
            product_view(user.telegram_id, value)
    elif 'AddProduct' in button_press:
        try:
            bot.deleteMessage(edit_message)
        except telepot.exception.TelegramError:
            pass
        finally:
            value = button_press.split()[1]
            add_product_to_order(user.telegram_id, value)
    elif 'BackProduct' in button_press:
        try:
            bot.deleteMessage(edit_message)
        except telepot.exception.TelegramError:
            pass
        finally:
            create_order(user.telegram_id, only_view=True)
    elif 'Payment' in button_press:
        try:
            bot.deleteMessage(edit_message)
        except telepot.exception.TelegramError:
            pass
        finally:
            value = button_press.split()[1]
            payment_telegram(user.telegram_id, value)


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
                inline_keyboard=[
                    [InlineKeyboardButton(text='Забронировать  🎉', callback_data=f'DoReserve {table.id}')]]
            )
        else:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[[]]
            )

            message += '\n\n*сейчас столик занят*'

        bot.sendPhoto(chat_id=user.telegram_id, photo=table.tableinfo.photo,
                      caption=message, reply_markup=keyboard)


def create_order(telegram_id, table_id=None, only_view=False):
    user = TelegramUser.objects.get(telegram_id=telegram_id)

    telegram_token = Settings.objects.first().telegram_token
    bot = telepot.Bot(telegram_token)

    if not only_view:
        table = Table.objects.get(id=table_id)

        table.is_free = False

        secret_uuid = uuid.uuid4()

        table.url = secret_uuid
        table.save()

        order = Order.objects.create(table_id=table, order_id=secret_uuid)

        user.order_id = order.order_id
        user.save()

    categories = ProductCategory.objects.all()
    order = Order.objects.get(order_id=user.order_id)

    message = 'Главное меню 🍱'

    keyboard = []

    for category in categories:
        keyboard.append([InlineKeyboardButton(text=f'🏷 {category.name}', callback_data=f'ViewCategory {category.id}')])

    if order.products:
        count = order.products.all().aggregate(sum=Sum('cost')).get('sum', 0)
        if count is None:
            count = 0

        if count != 0:
            keyboard.append([InlineKeyboardButton(text=f'Оплатить ({count} руб.) 💵',
                                                  callback_data=f'Payment {order.order_id}')])

    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)

    bot.sendMessage(chat_id=user.telegram_id, text=message, reply_markup=keyboard)


def product_view(telegram_id, value):
    telegram_token = Settings.objects.first().telegram_token
    bot = telepot.Bot(telegram_token)

    user = TelegramUser.objects.get(telegram_id=telegram_id)
    order = Order.objects.get(order_id=user.order_id)

    category = ProductCategory.objects.get(id=value)

    message = f'🏷 {category.name} 🏷'

    products = Product.objects.filter(category=category)

    keyboard = []

    for product in products:
        keyboard.append([InlineKeyboardButton(text=f' 🍽  {product.name}', callback_data=f'AddProduct {product.id}')])

    keyboard.append([InlineKeyboardButton(text='🔙  Назад', callback_data='BackProduct')])
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)

    bot.sendMessage(chat_id=user.telegram_id, text=message, reply_markup=keyboard)


def add_product_to_order(telegram_id, value):
    telegram_token = Settings.objects.first().telegram_token
    bot = telepot.Bot(telegram_token)

    user = TelegramUser.objects.get(telegram_id=telegram_id)
    order = Order.objects.get(order_id=user.order_id)

    product = Product.objects.get(id=value)

    product_order = ProductOrder()
    product_order.order = order
    product_order.product = product
    product_order.save()

    bot.sendMessage(chat_id=user.telegram_id, text='Добавлено!')
    create_order(telegram_id, only_view=True)


def payment_telegram(telegram_id, value):
    telegram_token = Settings.objects.first().telegram_token
    bot = telepot.Bot(telegram_token)

    user = TelegramUser.objects.get(telegram_id=telegram_id)

    order = Order.objects.get(order_id=value)

    conf = Settings.objects.last()

    Configuration.account_id = conf.account_id
    Configuration.secret_key = conf.secret_key

    cost = round(order.products.all().aggregate(sum=Sum('cost')).get('sum'), 2)

    payment = Payment.create(
        {
            'amount': {
                'value': '{}'.format(cost),
                'currency': 'RUB'
            },
            'confirmation': {
                'type': 'redirect',
                'return_url': 'http://127.0.0.1:8000/'
            },
            'capture': True,
            'description': 'Оплата заказа'
        }
    )

    message = f'Оплати свой заказ № {order.id}\n'

    ModelPayment.objects.create(
        order_id=order.order_id,
        table_id=order.table_id,
        payment_id=payment.id,
        status=payment.status,
        info='Оплата заказа',
        cost=round(cost)
    )

    keyboard = [[InlineKeyboardButton(text='Оплатить 💳', url=payment.confirmation.confirmation_url)]]

    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
    bot.sendMessage(chat_id=user.telegram_id, text=message, reply_markup=keyboard)


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
