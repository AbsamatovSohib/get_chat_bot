from telegram import ReplyKeyboardMarkup, Update, Bot, KeyboardButton
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
    CallbackQueryHandler
)

import logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

from datetime import datetime, timedelta
import pytz
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from quiz.models import User, Text
API_TOKEN = '7183505723:AAEzCfQf1dfEGyCPEpWkmvmx0ZUPv0xgYYk'
CHAT_ID = '4233894523'

ALL_CHAT = "Barcha chatlar"
INFO = "ID bo'yicha chat"
ALL_USERS = "Barcha username"
ALL_ID = "Barcha id"
NUMBER = "Userlar soni"

MAIN_KEYBOARD = [[ALL_USERS, ALL_ID], [INFO, NUMBER]]


def start(update, context: CallbackContext):

    update.message.reply_text(
        "Assalomu alaykum botga xush kelibsiz",
        reply_markup=ReplyKeyboardMarkup(
            MAIN_KEYBOARD,
            one_time_keyboard=False,
            input_field_placeholder="Quyidagilardan birini tanlang",
            resize_keyboard=True
        ),
    )


def get_file(update, context: CallbackContext):

    update.message.reply_text(
        "Assalomu alaykum botga xush kelibsiz",
        reply_markup=ReplyKeyboardMarkup(
            MAIN_KEYBOARD,
            one_time_keyboard=False,
            input_field_placeholder="Quyidagilardan birini tanlang",
            resize_keyboard=True
        ),
    )




def users(update, context: CallbackContext):

    us = User.objects.values('firstname', 'username')

    text = ''
    for user in us:
        if 'username' in user:
            text += "username: @" + user['username'] + " "
        text += "firstname: " + user['firstname'] + " \n"

    update.message.reply_text(
        text,
        )


def ids(update, context: CallbackContext):
    us = User.objects.values('user_id')

    text = ''
    for user in us:
        text += user['user_id'] + " \n"

    update.message.reply_text(
        text,
    )


IDDI = range(1)


def get_id(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Istalgan id ni kiriting"
    )

    return IDDI


def get_chat_by_id(update: Update, context: CallbackContext):
    id = update.message.text

    all = Text.objects.filter(user_id=id)

    text = ""
    for x in all:
        text += x.text + "  " + x.date + "\n"

    update.message.reply_text(
        text,
        reply_markup=ReplyKeyboardMarkup(
            MAIN_KEYBOARD,
            resize_keyboard=True)
    )

    return ConversationHandler.END


def number_of_people(update, context: CallbackContext):

    number = User.objects.count()

    update.message.reply_text(
        number,
        reply_markup=ReplyKeyboardMarkup(
            MAIN_KEYBOARD,
            one_time_keyboard=False,
            input_field_placeholder="Quyidagilardan birini tanlang",
            resize_keyboard=True
        ),
    )


def main():
    updater = Updater("6775673957:AAFn_1RR3Tj6_VTlPC5zGNh2o8GpgHBlMSc", use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            MessageHandler(Filters.text(ALL_USERS), users),
            MessageHandler(Filters.text(ALL_ID), ids),
            MessageHandler(Filters.text(INFO), get_id),
            MessageHandler(Filters.text(NUMBER), number_of_people),
            CommandHandler('file', get_file)
        ],
        states={
            IDDI: [
                MessageHandler(Filters.text & ~Filters.command, get_chat_by_id)
            ]
        },
        fallbacks=[

        ],
    )

    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

