import uuid

from django.db.models import Sum
from vk_api.bot_longpoll import VkBotEventType, VkBotEvent
from yookassa import Configuration, Payment

import vkbot.management.bot_keyboards as keys
import vkbot.management.texts as text
import vkbot.management.bot_commands as cmd
from orders.models import Order, ProductCategory
from payments.models import Payment as ModelPayment

from vkbot.management.bot_settings import vk
from vkbot.management.bot_settings import longpoll

import json

from restaurant.models import Table, TableInfo, Settings
from vkbot.models import *


def _vk_edit_message(event, message: str, keyboard=None, template=None, forward: str = ""):
    vk.messages.sendMessageEventAnswer(
        event_id=event.obj.event_id,
        peer_id=event.obj.peer_id,
        user_id=event.obj.user_id
    )

    if keyboard:
        vk.messages.edit(
            peer_id=event.obj.peer_id,
            message=message,
            keyboard=keyboard,
            conversation_message_id=event.obj.conversation_message_id,
            forward_messages=forward,
            random_id=0)

    elif template:
        vk.messages.edit(
            peer_id=event.obj.peer_id,
            message=message,
            conversation_message_id=event.obj.conversation_message_id,
            template=template,
            random_id=0)

    else:
        vk.messages.edit(
            event_id=event.object.event_id,
            peer_id=event.obj.peer_id,
            conversation_message_id=event.obj.conversation_message_id,
            message=message,
            random_id=0)


def main():
    print("VkBot loaded")

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            resolve_commands(event)

        elif event.type == VkBotEventType.MESSAGE_EVENT:
            resolve_msg_events(event)


def resolve_msg_events(event):
    user_id = event.object.user_id
    payload = event.object.get("payload")

    command = ""

    if payload:
        command = payload.get("command")

    if command == cmd.CHOOSE_TABLE:
        edit_tables_and_send_orders(event, user_id, payload.get("table_id"))


def resolve_commands(event):
    user_id = event.message.from_id
    payload = event.message.get("payload")

    command = ""
    msg_text = event.message.text

    if payload:
        payload = json.loads(payload)
        command = payload.get("command")

    # Possible commands
    if command == cmd.MENU or msg_text == cmd.MENU or msg_text == "начать":
        main_menu(user_id)
    elif command == cmd.ORDER:
        order_start(user_id, 0)
    elif command == cmd.BOOK:
        book(user_id)
    elif command == cmd.CHOOSE_TABLE:
        order_start(user_id, payload.get("table_id"))

    elif command == cmd.CLEAR:
        clear_user(user_id)

    elif command == cmd.FINISH:
        checkout(user_id)

    elif command == cmd.CHECK_ORDER:
        check_order(user_id)

    else:
        print(command)


def main_menu(user_id: int):
    vk.messages.send(
        user_id=user_id,
        message=text.TEXT_MAIN_MENU,
        keyboard=keys.keyboard_main_menu().get_keyboard(),
        random_id=0
    )


def clear_user(user_id: int):
    client = ClientVK.objects.filter(user_id=user_id).first()
    if client:
        client.delete()
        main_menu(user_id)
    else:
        notify(user_id, text.ERROR_NO_USER_FOUND)
        main_menu(user_id)


def get_payment_url(order_id):
    order = Order.objects.filter(order_id=order_id).first()

    if order is None:
        return None

    table_id = order.table_id

    cost = order.products.all().aggregate(sum=Sum('cost')).get('sum')
    info = text.PAYMENT_TEXT % order_id

    settings = Settings.objects.last()

    Configuration.account_id = settings.account_id
    Configuration.secret_key = settings.secret_key

    payment = Payment.create(
        {
            'amount': {
                'value': '{}'.format(round(cost, 2)),
                'currency': 'RUB'
            },
            'confirmation': {
                'type': 'redirect',
                'return_url': 'https://vk.com/public209490298/'
            },
            'capture': True,
            'description': info
        }
    )

    ModelPayment.objects.create(
        order_id=order_id,
        table_id=table_id,
        payment_id=payment.id,
        status=payment.status,
        info=info,
        cost=float(cost)
    )

    return payment.confirmation.confirmation_url


# do later
def checkout(user_id: int):
    pass


# do later
def check_order(user_id: int):
    pass


def notify(user_id: int, notify_text: str):
    vk.messages.send(
        user_id=user_id,
        message=notify_text,
        random_id=0
    )


def order_start(user_id: int, table_id):
    table = Table.objects.filter(id=table_id).first()

    if table is None:
        notify(user_id, text.ERROR_NO_TABLE_WITH_THIS_ID)
        return

    table.is_free = False
    secret_uuid = uuid.uuid4()
    table.url = secret_uuid
    table.save()
    order = Order.objects.create(table_id=table, order_id=secret_uuid)

    ClientVK.objects.create(user_id=user_id, order=order)

    vk.messages.send(
        user_id=user_id,
        message=text.TEXT_ORDER_START,
        keyboard=keys.keyboard_order().get_keyboard(),
        random_id=0
    )

    order_make(user_id)


def edit_tables_and_send_orders(event, user_id, table_id):
    table = TableInfo.objects.filter(table_id=table_id).first()

    if table:
        _vk_edit_message(event, text.TEXT_BOOK_SUCCESS % table.name)
        order_start(user_id, table_id)

    else:
        notify(user_id, text.ERROR_NO_TABLE_WITH_THIS_ID)


def order_end(user_id: int):
    vk.messages.send(
        user_id=user_id,
        message=text.TEXT_ORDER_END,
        random_id=0
    )


# do later
def refresh_order(user_id: int):
    client = ClientVK.objects.filter(user_id=user_id).first()
    pass


def order_make(user_id: int):
    all_products = _get_all_products_by_category()

    if all_products:
        for category in all_products:
            products = all_products.get(category)
            for some_products in divide_list_by_value(products, 10):
                vk.messages.send(
                    user_id=user_id,
                    message=text.TEXT_CATEGORY % category,
                    template=keys.carousel_order(some_products),
                    random_id=0
                )

    else:
        notify(user_id, text.ERROR_NO_PRODUCTS)


def book(user_id: int):
    tables = _get_all_tables()

    if tables:
        for table_list in divide_list_by_value(tables, 10):
            vk.messages.send(
                user_id=user_id,
                message=text.TEXT_BOOK_TABLE,
                template=keys.carousel_tables(table_list),
                random_id=0
            )

    else:
        notify(user_id, text.ERROR_NO_FREE_TABLES)


def divide_list_by_value(some_list, value):
    res = []
    for i in range(0, (len(some_list) % value)):
        _starting = i * value
        if _starting > len(some_list):
            break

        res.append(some_list[_starting:_starting + value])

    print(res)
    return res


def _get_all_products_by_category():
    products = ProductVk.objects.all()
    res = {}

    for item in products:
        val = item.product.category.name

        if res.get(val) is None:
            res[val] = []

        res[val].append(item)

    return res


def _get_all_tables():
    tables = TableVk.objects.all()
    res = []

    for item in tables:
        if item.table.table_id.is_free:
            res.append(item)

    return res


main()
