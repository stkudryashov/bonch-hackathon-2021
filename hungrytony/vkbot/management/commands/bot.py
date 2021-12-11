from vk_api.bot_longpoll import VkBotEventType, VkBotEvent

import vkbot.management.bot_keyboards as keys
import vkbot.management.texts as text
import vkbot.management.bot_commands as cmd

from vkbot.management.bot_settings import vk
from vkbot.management.bot_settings import longpoll

import json

from restaurant.models import Table


def main():
    print("VkBot loaded")
    tables = Table.objects.all()
    print(repr(tables))
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
        order(user_id)
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


def order(user_id: int):
    vk.messages.send(
        user_id=user_id,
        message=text.KEYS_MAIN_ORDER_NO_TABLE,
        random_id=0
    )


def book(user_id: int):
    vk.messages.send(
        user_id=user_id,
        message=text.KEYS_MAIN_BOOK_TABLE,
        random_id=0
    )


main()
