import os
from pprint import pprint

from finder import Finder
from vkbot import VkBot

if __name__ == '__main__':
    my_token = os.getenv("PERSONAL_TOKEN")
    finder = Finder(my_token)
    result = finder.find_matches(18, 25, 122, 1, 6)
    pprint(result)
    #bot_token = os.getenv("BOT_TOKEN")
    #vkbot = VkBot(bot_token)
    #vkbot.message_polling()


