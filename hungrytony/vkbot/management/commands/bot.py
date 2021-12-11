import uuid

from vk_api.bot_longpoll import VkBotEventType, VkBotEvent

import vkbot.management.bot_keyboards as keys
import vkbot.management.texts as text
import vkbot.management.bot_commands as cmd
from orders.models import Order

from vkbot.management.bot_settings import vk
from vkbot.management.bot_settings import longpoll

import json

from restaurant.models import Table


#     tables = Table.objects.all()

def main():
    print("VkBot loaded")

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            resolve_commands(event)


def resolve_commands(event):
    user_id = event.message.from_id
    payload = event.message.get("payload")

    command = ""
    msg_text = event.message.text

    if payload:
        payload = json.loads(payload)
        command = payload.get("command")
    else:
        command = msg_text.lower()

    # Possible commands
    if command == cmd.MENU:
        main_menu(user_id)
    elif command == cmd.ORDER:
        order_start(user_id)
    elif command == cmd.BOOK:
        book(user_id)
    else:
        print(command)


def main_menu(user_id: int):
    vk.messages.send(
        user_id=user_id,
        message=text.TEXT_MAIN_MENU,
        keyboard=keys.main_menu().get_keyboard(),
        random_id=0
    )
    vk.messages.send(
        user_id=user_id,
        message=text.TEXT_MAIN_MENU,
        template=
        {
            "type": "carousel",
            "elements": [{
                "photo_id": "-109837093_457242811",
                "action": {
                    "type": "open_photo"
                },
                "buttons": [{
                    "action": {
                        "type": "text",
                        "label": "Текст кнопки 🌚",
                        "payload": "{}"
                    }
                }]
            },
                {
                    "photo_id": "-109837093_457242811",
                    "action": {
                        "type": "open_photo"
                    },
                    "buttons": [{
                        "action": {
                            "type": "text",
                            "label": "Текст кнопки 2",
                            "payload": "{}"
                        }
                    }]
                },
                {
                    "photo_id": "-109837093_457242811",
                    "action": {
                        "type": "open_photo"
                    },
                    "buttons": [{
                        "action": {
                            "type": "text",
                            "label": "Текст кнопки 3",
                            "payload": "{}"
                        }
                    }]
                }
            ]
        },
        random_id=0
    )


def order_start(user_id: int):
    table = Table.objects.get(id=1)

    table.is_free = False

    secret_uuid = uuid.uuid4()
    table.url = secret_uuid
    table.save()
    Order.objects.create(table_id=table, order_id=secret_uuid)

    # order = Order.objects.get(order_id=secret_uuid)
    # product = request.POST.get('product_id')
    #
    # order.products.add(product)

    vk.messages.send(
        user_id=user_id,
        message=text.TEXT_ORDER_START,
        random_id=0
    )


def order_end(user_id: int):
    vk.messages.send(
        user_id=user_id,
        message=text.TEXT_ORDER_END,
        random_id=0
    )


def book(user_id: int):
    vk.messages.send(
        user_id=user_id,
        message=text.KEYS_MAIN_BOOK_TABLE,
        random_id=0
    )


main()
