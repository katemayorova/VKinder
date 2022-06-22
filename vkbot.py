import re
from random import randrange
from typing import List

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from persistence import SearchDao
from user import User


class VkBot:
    __FIRST_MATCH_PATTERN = r"^знакомства\s(\d+)\s(\d+)\s([м|ж])\s(\w+)$"
    __NEXT_MATCH_PATTERN = r"^далее$"

    def __init__(self, token, callback, search_dao: SearchDao):
        print("Создан объект бота!")
        self._COMMANDS = ["ЗНАКОМСТВА"]
        self.vk = vk_api.VkApi(token=token)
        self.long_poll = VkLongPoll(self.vk)
        self.callback = callback
        self.search_dao = search_dao

    def send_message(self, user_id, text):
        self.vk.method('messages.send', {'user_id': user_id, 'message': text, 'random_id': randrange(10 ** 7)})

    def message_polling(self):
        for event in self.long_poll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                if re.match(self.__FIRST_MATCH_PATTERN, event.text):
                    self.__first_match(event)
                elif re.match(self.__NEXT_MATCH_PATTERN, event.text):
                    self.__next_match(event)
                else:
                    response = "Этим ботом нужно пользоваться так:\n" \
                               "  знакомства <возраст от> <возраст до> <пол (м/ж)> <город>\n" \
                               "или если вы уже запрашивали, можно получить следующий результат:\n" \
                               "  далее"
                    self.send_message(event.user_id, response)

    def __first_match(self, event):
        result = re.match(self.__FIRST_MATCH_PATTERN, event.text)
        if result:
            age_from = result.group(1)
            age_to = result.group(2)
            sex = result.group(3)
            city = result.group(4)
            self.search_dao.save_search(event.user_id, age_from, age_to, sex, city)
            self.callback(event.user_id, age_from, age_to, sex, city)

    def __next_match(self, event):
        result = self.search_dao.get_search(event.user_id)
        if result is None:
            response = "Вы еще ничего не искали"
            self.send_message(event.user_id, response)
        else:
            age_from, age_to, sex, city = result[1], result[2], result[3], result[4]
            self.callback(event.user_id, age_from, age_to, sex, city)

    def send_user(self, user_id, user: User):
        message = f'{user.surname} {user.name} ({user.sex})\n' \
                  f'https://vk.com/id{user.vk_id}'
        self.vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7),
                                         'attachment': ",".join(user.top_photos)})

    def send_users(self, user_id, users: List):
        for user in users:
            self.send_user(user_id, user)
