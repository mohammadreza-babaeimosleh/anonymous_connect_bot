import os

import emoji
from loguru import logger
from telebot import types

from src.bot import bot
from src.constant import keyboards, keys, states
from src.db import db
from src.filters import IsAdmin
from src.utils.io import write_json


class Bot:
    """Telegram bot to randomly connect to strangers to talk
    """

    def __init__(self, telebot) -> None:
        self.bot = telebot

        self.bot.add_custom_filter(IsAdmin())

        self.db = db

        self.handlers()

    def handlers(self):
        @self.bot.message_handler(regexp=emoji.emojize(keys.random_connect))
        def random_connect(message):
            """connecting random strangers to each other
            """
            self.send_message(
                message.chat.id,
                ":busts_in_silhouette: <strong> Connecting you to a random person.... </strong>",
                reply_markup=keyboards.exit,
            )

            # finding another person to connect and setting states
            self.update_state(message.chat.id, states.random_connect)

            other_user = self.db.users.find_one(
                {"state": states.random_connect, "chat.id": {"$ne": message.chat.id}}
            )

            if not other_user:
                return

            # setting states for user
            self.update_state(other_user["chat"]["id"], states.connected)
            self.send_message(
                other_user["chat"]["id"], f"connected to user {message.chat.id}..."
            )

            # settign states for other connected user
            self.update_state(message.chat.id, states.connected)
            self.send_message(
                message.chat.id, f'connected to user {other_user["chat"]["id"]}...'
            )

            # store connected persons ids
            self.db.users.update_one(
                {"chat.id": message.chat.id},
                {"$set": {"connected_to": other_user["chat"]["id"]}},
            )

            self.db.users.update_one(
                {"chat.id": other_user["chat"]["id"]},
                {"$set": {"connected_to": message.chat.id}},
            )

        @self.bot.message_handler(regexp=emoji.emojize(keys.exit))
        def exit(message):
            """setting exit keyboard up
            """
            self.send_message(
                message.chat.id, "exited from chat", reply_markup=keyboards.main
            )
            self.update_state(message.chat.id, states.main)

            connected_to = self.db.users.find_one({"chat.id": message.chat.id})

            if not connected_to:
                return

            other_user_id = connected_to["connected_to"]

            self.update_state(other_user_id, states.main)
            self.send_message(other_user_id, keys.exit, reply_markup=keyboards.main)
            self.send_message(
                other_user_id, "exited from chat", reply_markup=keyboards.main
            )

            self.db.users.update_one(
                {"chat.id": message.chat.id}, {"$set": {"connected_to": None}}
            )
            self.db.users.update_one(
                {"chat.id": other_user_id}, {"$set": {"connected_to": None}}
            )

        @bot.message_handler(commands=["start"])
        def start(message):
            """method for handling /start command and registering new users
            """
            bot.send_message(
                message.chat.id,
                f"Howdy, how are you doing <strong>{message.chat.first_name}</strong>",
                reply_markup=keyboards.main,
            )

            self.db.users.update_one(
                {"chat.id": message.chat.id}, {"$set": message.json}, upsert=True
            )

        @self.bot.message_handler(is_admin=True)
        def admin_of_group(message):
            """check if senderof message is admin or not
            """
            self.send_message(
                message.chat.id, f"<strong>You are admin of group</strong>"
            )

        @self.bot.message_handler(func=lambda _: True)
        def echo_all(message):
            """method for handling messages between to connected users 
            """
            user = self.db.users.find_one({"chat.id": message.chat.id})
            if (
                not user
                or user["state"] != states.connected
                or user["connected_to"] is None
            ):
                self.send_message(
                    message.chat.id, "Unkown Command", reply_markup=keyboards.main
                )
                return

            self.send_message(
                user["connected_to"], message.text, reply_markup=keyboards.exit
            )

    def run(self):
        """starting bot
        """
        logger.info("bot started")
        self.bot.infinity_polling()

    def send_message(self, chat_id, text, reply_markup=None, emojize=True):
        """helper method for sending differend messages

        Args:
            chat_id (int): id of target user
            text (str): message to send
            reply_markup (markup, optional): desierd keyboard to pop up after sending message. Defaults to None.
            emojize (bool, optional): interpereting emojies. Defaults to True.
        """
        if emojize:
            text = emoji.emojize(text)

        self.bot.send_message(chat_id, text, reply_markup=reply_markup)

    def update_state(self, user_id, state):
        """helper method to update state of different users

        Args:
            user_id (int): id of user 
            state (str): the current state of user to update
        """
        self.db.users.update_one(
            {"from.id": user_id}, {"$set": {"state": state}}, upsert=True
        )


if __name__ == "__main__":
    bot = Bot(telebot=bot)
    bot.run()
