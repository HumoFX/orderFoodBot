from django_telegrambot.apps import DjangoTelegramBot
from telegram.ext import MessageHandler, Filters, CallbackContext, CallbackQueryHandler
from telegram import Update
from bot import constants
from bot.base_commands import register
from bot.controller import Controller
from bot.models import TelegramUser, Command
from product.models import TelegramChat


def bot_control(update: Update, context: CallbackContext):
    if update.message.chat.type == 'private':
        user_id = update.message.chat.id
    else:
        user_id = update.message.from_user.id
        chat, created = TelegramChat.objects.get_or_create(telegram_id=update.message.chat.id)
        if created:
            chat.title = update.message.chat.title
            chat.type = update.message.chat.type
            chat.save()

    user, created = TelegramUser.objects.get_or_create(
        telegram_id=user_id)
    if created:
        user.first_name = update.message.from_user.first_name
        user.last_name = update.message.from_user.last_name
        user.username = update.message.from_user.username
        user.save()
    try:
        cart = user.cart.filter(active=True)
    except:
        cart = None
    if not user.is_registered:
        register(context.bot, user, update)

    elif update.message.text == '/start':
        Controller(context.bot, update, user).start()

    try:
        last_command = Command.objects.filter(user=user).last()
    except Command.DoesNotExist:
        last_command = None

    if update.message.text == 'Home':
        Controller(context.bot, update, user).go_home()

    elif update.message.text in ["Orqaga", 'Back', "Назад", "orqaga", 'back', "назад"]:
        Controller(context.bot, update, user).go_home()

    elif last_command.to_menu == constants.language:
        Controller(context.bot, update, user, cart, last_command).language_select()

    elif last_command.to_menu == constants.category:
        Controller(context.bot, update, user, cart, last_command).category_select()

    elif last_command.to_menu == constants.product:
        Controller(context.bot, update, user, cart, last_command).product_select()

    elif last_command.to_menu == constants.pieces:
        Controller(context.bot, update, user, cart, last_command).pieces_select()

    elif last_command.to_menu == constants.add_to_cart:
        Controller(context.bot, update, user, cart, last_command).add_to_card()

    elif last_command.to_menu == constants.cart:
        Controller(context.bot, update, user, cart, last_command).cart_select()

    elif last_command.current_menu == constants.proceed_to_order:
        Controller(context.bot, update, user, cart, last_command).location()

    elif last_command.to_menu == constants.remove_from_cart:
        Controller(context.bot, update, user, cart, last_command).remove_from_cart()

    elif last_command.to_menu == constants.checkout:
        Controller(context.bot, update, user, cart, last_command).checkout()

    elif last_command.to_menu == constants.location:
        Controller(context.bot, update, user, cart, last_command).location()

    elif last_command.to_menu == constants.payment_method:
        Controller(context.bot, update, user, cart, last_command).payment_method()

    elif last_command.to_menu == constants.confirm_order:
        Controller(context.bot, update, user, cart, last_command).confirm_order()

    elif last_command.to_menu == constants.order_succeed:
        Controller(context.bot, update, user, cart, last_command).order_succeed()

    elif last_command.to_menu == constants.order_failed:
        Controller(context.bot, update, user, cart, last_command).order_fail()

    elif last_command.to_menu == constants.order_canceled:
        Controller(context.bot, update, user, cart, last_command).order_cancel()

    elif last_command.to_menu == constants.payment_method:
        Controller(context.bot, update, user, cart, last_command).finish_order()

    elif last_command.to_menu == constants.finish_order:
        Controller(context.bot, update, user, cart, last_command).finish_order()

    elif last_command.current_menu == constants.feedback:
        Controller(context.bot, update, user, cart, last_command).feedback()

    elif last_command.to_menu == constants.home:
        Controller(context.bot, update, user, cart, last_command).home_control()

    else:
        context.bot.sendMessage(update.message.chat_id, text='???')


def admin_control(update: Update, context: CallbackContext):
    print(update.callback_query.data)
    user_id = update.callback_query.from_user.id
    user, created = TelegramUser.objects.get_or_create(
        telegram_id=user_id)
    if created:
        user.first_name = update.message.from_user.first_name
        user.last_name = update.message.from_user.last_name
        user.username = update.message.from_user.username
        user.save()
    if update.callback_query:
        return Controller(context.bot, update, user).change_status()


def main():
    dp = DjangoTelegramBot.dispatcher
    dp.add_handler(MessageHandler(Filters.all, bot_control))

    dp.add_handler(CallbackQueryHandler(admin_control))

    # dp.add_handler(MessageHandler(Filters.sticker, sticker))
