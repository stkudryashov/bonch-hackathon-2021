from vk_api.keyboard import VkKeyboard, VkKeyboardColor as colors

import vkbot.management.texts as text
import vkbot.management.bot_commands as command


def main_menu() -> VkKeyboard:
    keyboard = VkKeyboard()

    keyboard.add_button(text.KEYS_MAIN_BOOK_TABLE, colors.PRIMARY, payload={"command": command.BOOK})
    keyboard.add_button(text.KEYS_MAIN_ORDER_NO_TABLE, colors.SECONDARY, payload={"command": command.ORDER})

    return keyboard



