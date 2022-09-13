import os

import telebot

# initializing bot with token
bot = telebot.TeleBot(os.environ["anonymous_bot_token"], parse_mode="HTML")
