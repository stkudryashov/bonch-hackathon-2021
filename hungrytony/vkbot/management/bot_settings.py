import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import os
from restaurant.models import Settings

# Ключи авторизации.
token = Settings.objects.first().vk_token
vk_group_id = "209490298"


vk_session = vk_api.VkApi(token=token, api_version="5.131")
vk_session._auth_token()

vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, vk_group_id)
