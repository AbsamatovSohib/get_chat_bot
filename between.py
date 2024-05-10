# import threading
# import time
# from telegram.ext import (
#     Updater,
#     CommandHandler,
#     MessageHandler,
#     Filters,
#     ConversationHandler,
#     CallbackContext,
#     CallbackQueryHandler
# )
#
#
# import schedule
# import requests
#
# from datetime import datetime, timedelta
# import pytz
# import os, django
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
# django.setup()
#
# from quiz.models import User, Text
# API_TOKEN = '7183505723:AAEzCfQf1dfEGyCPEpWkmvmx0ZUPv0xgYYk'
# CHAT_ID = '4233894523'
#
#
# # def run_continuously(interval=1):
# #
# #     cease_continuous_run = threading.Event()
# #
# #     class ScheduleThread(threading.Thread):
# #         @classmethod
# #         def run(cls):
# #             while not cease_continuous_run.is_set():
# #                 schedule.run_pending()
# #                 time.sleep(2)
# #
# #     continuous_thread = ScheduleThread()
# #     continuous_thread.start()
# #     return cease_continuous_run
#
#
# def background_job():
#     url = f'https://api.telegram.org/bot{API_TOKEN}/getUpdates'
#
#     # params = {
#     #     CHAT_ID: CHAT_ID
#     # }
#     # response = requests.get(url, params=params)
#
#     print("aaa")
#     response = requests.get(url)
#     if response.ok:
#         chat_history = response.json()['result']
#         print(chat_history)
#         # print("++\n", chat_history, "\n++")
#
#         for mes in chat_history:
#             a = mes['update_id']
#             if 'message' not in mes.keys():
#                 continue
#             else:
#                 user = mes['message']['from']
#                 message = mes['message']
#                 user_id = user['id']
#
#                 timestamp = datetime.utcfromtimestamp(mes['message']['date'])
#                 dt_object = timestamp
#                 original_timezone = pytz.utc
#                 dt_object = original_timezone.localize(dt_object)
#                 original_date = dt_object + timedelta(hours=5)
#
#                 if 'last_name' in user.keys():
#                     lastname = user['last_name']
#                 if 'username' in user.keys():
#                     username = user['username']
#
#                 all_users = User.objects.values('user_id')
#
#                 if {"user_id": f"{user_id}"} not in all_users:
#                     User.objects.create(user_id=user_id, firstname=user['first_name'],
#                                         lastname=lastname, username=username)
#
#                 if 'text' in message.keys():
#                     text_info = {'text': f"{mes['message']['text']}", "date": f"{original_date}"}
#
#                     if text_info not in Text.objects.values("text", "date"):
#                         Text.objects.create(user_id=user_id, text=mes['message']['text'], date=original_date)
#
#             print("Job has finished")
#     else:
#         print('Failed to retrieve chat history:', response.text)
#
#
# # schedule.every(10).seconds.do(background_job)
# # stop_run_continuously = run_continuously()
#
#
# def start(update, context):
#     update.message.reply_text('Bot started!')
#
# # Initialize the updater and dispatcher
# updater = Updater(API_TOKEN, use_context=True)
# dispatcher = updater.dispatcher
#
# # Add the command handler for the /start command
# dispatcher.add_handler(CommandHandler("start", start))
#
# # Start the bot in a separate thread
# def run_bot():
#     updater.start_polling()
#     updater.idle()
#
# bot_thread = threading.Thread(target=run_bot)
# bot_thread.start()
#
# # Start the getUpdates thread
# updates_thread = threading.Thread(target=background_job)
# updates_thread.start()