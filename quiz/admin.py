from django.contrib import admin
from quiz.models import User, Text, TelegramFile


admin.site.register(User)
admin.site.register(Text)
admin.site.register(TelegramFile)
