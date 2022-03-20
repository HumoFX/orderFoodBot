from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from bot import constants
from product.models import Category, Product


def back_markup(lang):
    return ReplyKeyboardMarkup([
        [constants.messages[lang][constants.back_menu]]
    ], resize_keyboard=True)


def finish_order_markup(lang, product_list):
    return ReplyKeyboardMarkup([
        # [constants.messages[lang][constants.clear_cart]],
        [constants.messages[lang][constants.proceed_to_order]],
        *product_list,
        [constants.messages[lang][constants.back_menu]]
    ], resize_keyboard=True, width=1)


register_markup = ReplyKeyboardMarkup([
    [KeyboardButton(text=constants.send_contact_menu, request_contact=True)]
], resize_keyboard=True)


# create location_markup to handle location
def location_markup(lang):
    location = ReplyKeyboardMarkup([
        [KeyboardButton(text=constants.messages[lang][constants.send_location], request_location=True)]
    ], resize_keyboard=True)
    return location


# create checkout markup for confirmation
def checkout_markup(lang):
    checkout = [
        [constants.messages[lang][constants.confirm_order]],
        [constants.messages[lang][constants.not_confirm_order]]
    ]
    return ReplyKeyboardMarkup(checkout, resize_keyboard=True, width=2)


def home_markup(lang):
    home = [
        [constants.messages[lang][constants.make_order_menu]],
        [constants.messages[lang][constants.cart_menu],
         constants.messages[lang][constants.feedback_menu]],
        [constants.messages[lang][constants.language_menu]]
    ]
    return ReplyKeyboardMarkup(home, resize_keyboard=True)


languages = [
    ["🇺🇿", "🇷🇺"]
]
languages_markup = ReplyKeyboardMarkup(languages, resize_keyboard=True)


def categories_markup(lang):
    if lang == 'en':
        categories = list(Category.objects.filter(
            available=True).values_list('name_en', flat=True))
    elif lang == 'ru':
        categories = list(Category.objects.filter(
            available=True).values_list('name_ru', flat=True))
    else:
        categories = list(Category.objects.filter(
            available=True).values_list('name', flat=True))
    categories.append(constants.messages[lang][constants.back_menu])
    return ReplyKeyboardMarkup([categories[i:i + 2] for i in range(0, len(categories), 2)], resize_keyboard=True,
                               width=2)


def product_list(category_id, lang):
    if lang == 'en':
        products = list(Product.objects.filter(
            category_id=category_id, available=True).values_list('name_en', flat=True))
    elif lang == 'ru':
        products = list(Product.objects.filter(
            category_id=category_id, available=True).values_list('name_ru', flat=True))
    else:
        products = list(Product.objects.filter(
            category_id=category_id, available=True).values_list('name', flat=True))
    products.append(constants.messages[lang][constants.back_menu])
    return ReplyKeyboardMarkup([products[i:i + 2] for i in range(0, len(products), 2)], resize_keyboard=True)


def pieces_markup(lang):
    pieces = [str(x) for x in (range(1, 10))]
    pieces.append(constants.messages[lang][constants.back_menu])
    return ReplyKeyboardMarkup(
        [pieces[i:i + 3] for i in range(0, len(pieces), 3)], resize_keyboard=True, width=3)


def payment_markup(lang):
    payment = [
        [constants.messages[lang][constants.cash_payment]],
        [constants.messages[lang][constants.card_payment]]
    ]
    return ReplyKeyboardMarkup(payment, resize_keyboard=True, width=2)


# create inline keyboard for order status update for admin
def order_status_inline_markup(lang, status, order_id):
    if status == 1:
        status_list = [
            [InlineKeyboardButton(constants.messages[lang][constants.accept_order], callback_data=f'{order_id}:2'),
             InlineKeyboardButton(constants.messages[lang][constants.decline_order], callback_data=f'{order_id}:5')],
        ]
    elif status == 2:
        status_list = [
            [InlineKeyboardButton(constants.messages[lang][constants.send_order], callback_data=f'{order_id}:3')],
        ]
    elif status == 3:
        status_list = [
            [InlineKeyboardButton(constants.messages[lang][constants.delivered], callback_data=f'{order_id}:4')],
        ]
    elif status == 4:
        return None
    elif status == 5:
        return None
    return InlineKeyboardMarkup(status_list)


# create broadcast inline keyboard for admin
def broadcast_inline_markup(broadcast_id):
    status_list = [
        [InlineKeyboardButton('Опубликовать', callback_data=f'{broadcast_id}:2'),
         InlineKeyboardButton('Удалить', callback_data=f'{broadcast_id}:3')],
    ]
    return InlineKeyboardMarkup(status_list)


def products_markup(product_list, lang):
    products = [[product_list[i:i + 2] for i in range(0, len(product_list), 2)],
                [constants.messages[lang][constants.back_menu]]]
    return ReplyKeyboardMarkup(products, resize_keyboard=True, width=2)
