from django.db import models

from bot import constants
from bot.constants import LANGUAGES


class TelegramUser(models.Model):
    telegram_id = models.PositiveIntegerField()
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=16, null=True)
    step = models.PositiveSmallIntegerField(default=1)
    language = models.CharField(
        max_length=64, choices=LANGUAGES, default=constants.RU)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_registered = models.BooleanField(default=False)

    def __str__(self):
        return '{}, {}, {}'.format(self.telegram_id, self.phone_number, self.first_name)


class Feedback(models.Model):
    user = models.ForeignKey('TelegramUser', on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'From {}, {}'.format(self.user.telegram_id, self.text)


class Command(models.Model):
    user = models.ForeignKey('TelegramUser', on_delete=models.CASCADE)
    text = models.CharField(max_length=255, null=True, blank=True)
    from_menu = models.CharField(max_length=255, null=True, blank=True)
    current_menu = models.CharField(max_length=255, null=True, blank=True)
    to_menu = models.CharField(max_length=255, null=True, blank=True)
    message_id = models.PositiveIntegerField()
    category_id = models.PositiveIntegerField(null=True, blank=True)
    product_id = models.PositiveIntegerField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} {}'.format(self.user, self.text)
