import os

from finder import Finder
from user import User
from vkbot import VkBot


class Controller:
    __STATUS_ACTIVE_SEARCH = 6

    def __init__(self):
        my_token = os.getenv("PERSONAL_TOKEN")
        bot_token = os.getenv("BOT_TOKEN")
        self.finder = Finder(my_token)
        self.vkbot = VkBot(bot_token, self.on_match_request)

    def run(self):
        self.vkbot.message_polling()

    def on_match_request(self, vk_id, age_from, age_to, sex, city):
        city_id = self.finder.get_city_id(city)
        if city_id < 0:
            self.vkbot.send_messages(vk_id, f"Город \"{city}\" не найден")
        else:
            matches = self.finder.find_matches(
                age_from,
                age_to,
                city_id,
                User.SEX_MAPPING[sex],
                self.__STATUS_ACTIVE_SEARCH)
            self.vkbot.send_users(vk_id, matches)



