from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import TelegramUser, Feedback, Command

admin.site.register(TelegramUser)
admin.site.register(Feedback)
admin.site.register(Command)
