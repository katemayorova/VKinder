import re
from random import randrange
from typing import List

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from user import User


class VkBot:
    def __init__(self, token, callback):
        print("Создан объект бота!")
        self._COMMANDS = ["ЗНАКОМСТВА"]
        self.vk = vk_api.VkApi(token=token)
        self.long_poll = VkLongPoll(self.vk)
        self.callback = callback

    def send_messages(self, user_id, text):
        self.vk.method('messages.send', {'user_id': user_id, 'message': text, 'random_id': randrange(10 ** 7), 'attachment': 'photo497382519_456239018'})

    def message_polling(self):
        for event in self.long_poll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                pattern = r"знакомства\s(\d+)\s(\d+)\s([м|ж])\s(\w+)$"
                result = re.match(pattern, event.text)
                if result:
                    age_from = result.group(1)
                    age_to = result.group(2)
                    sex = result.group(3)
                    city = result.group(4)
                    self.callback(event.user_id, age_from, age_to, sex, city)
                else:
                    response = "Этим ботом нужно пользоваться так:\n" \
                               "  знакомства <возраст от> <возраст до> <пол (м/ж)> <город>"
                    self.send_messages(event.user_id, response)

    def send_user(self, user_id, user: User):
        message = f'{user.surname} {user.name} ({user.sex})\n' \
                  f'https://vk.com/id{user.vk_id}'
        self.vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7),
                                         'attachment': ",".join(user.top_photos)})

    def send_users(self, user_id, users: List):
        for user in users:
            self.send_user(user_id, user)
