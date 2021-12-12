import json

from vk_api.keyboard import VkKeyboard, VkKeyboardColor as colors
from vk_api.keyboard import VkKeyboardButton
import vkbot.management.texts as text
import vkbot.management.bot_commands as command


def keyboard_main_menu() -> VkKeyboard:
    keyboard = VkKeyboard()

    keyboard.add_button(text.KEYS_MAIN_BOOK_TABLE, colors.PRIMARY, payload={"command": command.BOOK})
    keyboard.add_button(text.KEYS_MAIN_ORDER_NO_TABLE, colors.SECONDARY, payload={"command": command.ORDER})

    return keyboard


def keyboard_order() -> VkKeyboard:
    keyboard = VkKeyboard()
    keyboard.add_button(text.KEYS_CHECK_ORDER, colors.PRIMARY, payload={"command": ""})
    keyboard.add_line()
    keyboard.add_button(text.KEYS_FINISH, colors.POSITIVE, payload={"command": ""})
    keyboard.add_line()
    keyboard.add_button(text.KEYS_CANCEL, colors.NEGATIVE, payload={"command": ""})

    return keyboard


def get_carousel_element(title: str = None, description: str = None, photo_id: str = None, buttons=None):
    carousel_element = {
        "title": title,
        "description": description,
        "photo_id": photo_id,
        "action": {
            "type": "open_photo"
        },
    }

    if buttons:
        carousel_element.update({"buttons": buttons})

    return carousel_element


def get_button(title, payload=None):
    _keyboard = VkKeyboard()
    _keyboard.add_callback_button(title, payload=payload)
    buttons = json.loads(_keyboard.get_keyboard()).get("buttons")[0]
    return buttons


def carousel_tables(list_of_vk_tables):
    res = {
        "type": "carousel",
        "elements": [get_carousel_element(x.table.name, x.table.info, '-' + x.vk_photo_id, get_button(text.KEYS_CHOOSE,
                                                                                                      {
                                                                                                          "command": command.CHOOSE_TABLE,
                                                                                                          "table_id": x.table.table_id.id}))
                     for x in list_of_vk_tables]
    }

    return json.dumps(res)


def carousel_order(list_of_vk_products):
    res = {
        "type": "carousel",
        "elements": [get_carousel_element(x.product.name, x.product.info, '-' + x.vk_photo_id,
                                          get_button(text.KEYS_CHOOSE, {"command": command.CHOOSE_PRODUCT,
                                                                        "order_id": str(x.product.id)}))
                     for x in list_of_vk_products]
    }

    return json.dumps(res)
