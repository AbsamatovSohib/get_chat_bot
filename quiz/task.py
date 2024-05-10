from celery import shared_task
import requests
from quiz.models import User, Text
from datetime import datetime, timedelta
import pytz
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)

API_TOKEN = '7183505723:AAEzCfQf1dfEGyCPEpWkmvmx0ZUPv0xgYYk'
CHAT_ID = '4233894523'


@shared_task()
def job():
    url = f'https://api.telegram.org/bot{API_TOKEN}/getUpdates'

    params = {
        CHAT_ID: CHAT_ID
    }
    response = requests.get(url, params=params)
    if response.ok:
        chat_history = response.json()['result']
        print("Sssssss")
        i = 1
        for mes in chat_history:
            a = mes['update_id']
            if 'message' not in mes.keys():
                continue
            else:
                user = mes['message']['from']
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

                i += 1
                if {"user_id": f"{user_id}"} not in all_users:
                    User.objects.create(user_id=user_id, firstname=user['first_name'],
                                        lastname=lastname, username=username)

                text_info = {'text': f"{mes['message']['text']}", "date": f"{original_date}"}

                if text_info not in Text.objects.values("text", "date"):
                    Text.objects.create(user_id=user_id, text=mes['message']['text'], date=original_date)
                    print("Saaaa")
    else:
        print('Failed to retrieve chat history:', response.text)


