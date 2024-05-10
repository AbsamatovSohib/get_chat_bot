import threading
import time

import schedule
import requests

from datetime import datetime, timedelta
import pytz
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from quiz.models import User, Text, TelegramFile
API_TOKEN = '7183505723:AAEzCfQf1dfEGyCPEpWkmvmx0ZUPv0xgYYk'
CHAT_ID = '4233894523'
from telegram import bot


def run_continuously(interval=1):

    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                # time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run


def background_job():
    url = f'https://api.telegram.org/bot{API_TOKEN}/getUpdates'

    # params = {
    #     CHAT_ID: CHAT_ID
    # }
    # response = requests.get(url, params=params)

    response = requests.get(url)
    if response.ok:
        chat_history = response.json()['result']
        # print("++\n", chat_history, "\n++")

        for mes in chat_history:
            a = mes['update_id']
            if 'message' not in mes.keys():
                continue
            else:
                user = mes['message']['from']
                message = mes['message']
                user_id = user['id']

                timestamp = datetime.utcfromtimestamp(mes['message']['date'])
                dt_object = timestamp
                original_timezone = pytz.utc
                dt_object = original_timezone.localize(dt_object)
                original_date = dt_object + timedelta(hours=5)

                if 'last_name' in user.keys():
                    lastname = user['last_name']
                if 'username' in user.keys():
                    username = user['username']

                all_users = User.objects.values('user_id')

                if {"user_id": f"{user_id}"} not in all_users:
                    User.objects.create(user_id=user_id, firstname=user['first_name'],
                                        lastname=lastname, username=username)

                if 'text' in message.keys():
                    text_info = {'text': f"{mes['message']['text']}", "date": f"{original_date}"}

                    if text_info not in Text.objects.values("text", "date"):
                        Text.objects.create(user_id=user_id, text=mes['message']['text'], date=original_date)

                if 'document' in message.keys():
                    doc = mes['message']['document']
                    # print(doc)
                    file_id = doc['file_id']
                    # print(file_id)
                    file_name = doc['file_name']
                    # print(file_name)
                    # file_url = f'https://api.telegram.org/bot{API_TOKEN}/getFile?file_id={file_id}'
                    # response = requests.get(file_url)
                    # file_path = response.json()['result']['file_path']
                    # file_url = f'https://api.telegram.org/file/bot{API_TOKEN}/{file_path}'



                    def download_file(file_id, file_name):
                        file_url = f'https://api.telegram.org/bot{API_TOKEN}/getFile?file_id={file_id}'
                        response = requests.get(file_url)
                        file_path = response.json()['result']['file_path']
                        file_url = f'https://api.telegram.org/file/bot{API_TOKEN}/{file_path}'
                        print(file_url)
                        with open(file_name, 'wb') as f:
                            print(f)
                            f.write(requests.get(file_url).content)
                        return file_path

                    def save_file_to_database(file_id, file_name, file_path):
                        # file = bot.get_file(file_id)
                        # file.download(file_name)
                        file_url = f'https://api.telegram.org/file/bot{API_TOKEN}/{file_path}'
                        telegram_file = TelegramFile.objects.create(
                            file_id=file_id,
                            file_name=file_name,
                            file_path=file_path,
                            file=file_url
                        )
                        return telegram_file
                    # TelegramFile.objects.create(file_id=file_id, file_name=file_name, file_path=file_path)
                    # with open(file_name, 'wb') as f:
                    #     f.write(requests.get(file_url).content)

                    file_path = download_file(file_id, file_name)
                    save_file_to_database(file_id, file_name, file_path)

            print("Job has finished")
    else:
        print('Failed to retrieve chat history:', response.text)


schedule.every().second.do(background_job)
stop_run_continuously = run_continuously()

