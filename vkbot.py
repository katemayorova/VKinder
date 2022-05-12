import requests as requests
from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType


class VkBot:
    def __init__(self, token):
        print("Создан объект бота!")
        self._COMMANDS = ["ЗНАКОМСТВА"]
        self.vk = vk_api.VkApi(token=token)
        self.long_poll = VkLongPoll(self.vk)

    def send_messages(self, user_id, text):
        self.vk.method('messages.send', {'user_id': user_id, 'message': text, 'random_id': randrange(10 ** 7)})

    def message_polling(self):
        for event in self.long_poll.listen():
            if event.type == VkEventType.MESSAGE_NEW:

                if event.to_me:
                    print(f'Получено сообщение "{event.text}" от пользователя "{event.user_id}"')
                    self.send_messages(event.user_id, event.text)








