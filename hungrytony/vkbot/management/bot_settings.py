import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import os

# Ключи авторизации.
token = "74d411a5559a9700d430067829639591a5b7698cbcfba6919eb7fbc328946327497827c7130981767e4ca"
vk_group_id = "209490298"


vk_session = vk_api.VkApi(token=token, api_version="5.131")
vk_session._auth_token()

vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, vk_group_id)
