import logging

from bot import constants, markups
from bot.models import Command

logger = logging.getLogger(__name__)


# create function to check if text is phone number with plus and digits only and return True or False
def is_phone_number(text):
    if text.startswith('+') and text[1:].isdigit():
        return True
    return False


def register(bot, user, update):
    if update.message.contact:
        user.phone_number = update.message.contact.phone_number
        user.is_registered = True
        user.save()
        bot.sendMessage(chat_id=user.telegram_id,
                        text=constants.register_succeed,
                        reply_markup=markups.home_markup('ru'))
        return Command.objects.create(user=user,
                                      message_id=update.message.message_id,
                                      text=constants.register,
                                      to_menu=constants.home)
    elif update.message.text and is_phone_number(update.message.text):
        user.phone_number = update.message.text
        user.is_registered = True
        user.save()
        bot.sendMessage(chat_id=user.telegram_id,
                        text=constants.register_succeed,
                        reply_markup=markups.home_markup('ru'))
        return Command.objects.create(user=user,
                                      message_id=update.message.message_id,
                                      text=constants.register,
                                      to_menu=constants.home)
    elif user.phone_number is None:
        bot.sendMessage(update.message.chat_id,
                        text=constants.ask_contact,
                        reply_markup=markups.register_markup)
        Command.objects.create(user=user,
                               message_id=update.message.message_id,
                               text=update.message.text,
                               to_menu=constants.home)

# def help_me(bot, update):
#     bot.sendMessage(update.message.chat_id, text='Call: 911')
#
#
# def sticker(bot, update):
#     bot.sendSticker(update.message.chat_id, sticker=update.message.sticker)
#
#
# def error(bot, update, errors):
#     logger.warning('Update "%s" caused error "%s"' % (update, errors))
