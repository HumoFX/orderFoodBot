# for user language choices
UZ = 'uz'
RU = 'ru'
LANGUAGES = [
    (UZ, "O'zbekcha"),
    (RU, 'Русский')
]

# for last command writing
register = 'register'
home = 'home'
category = 'category'
product = 'product'
language = 'language'
feedback = 'feedback'
pieces = 'pieces'
cart = 'cart'
add_to_cart = 'add to cart'
finish_order = 'finish_order'
back = 'back'

# for menus
make_order_menu = '🛒 Make order'
cart_menu = '🛒 Cart'
my_orders_menu = '🛍 My Orders'
language_menu = '🇺🇿 🇷🇺'
feedback_menu = '✍️ Feedback'
back_menu = 'Back'
finish_order_menu = 'Finish order'
send_contact_menu = "Поделится контактом"

# for messages
register_succeed = "Спасибо за регистрацию! Теперь вы можете пользоваться ботом."
ask_contact = "Отправьте ваш номер телефона"
welcome = 'Добро пожаловать!'
empty_cart = "Your cart is empty"
lang_select = "Language has changed"
feedback_succeed = 'Thanks for your feedback!'
feedback_send = 'Enter text below and send.'
in_your_cart = "In your cart:"
no_orders_yet = "You didn't order anything yet."
your_orders = "Your orders:"
status = 'Status'
ordered = 'Ordered'
delivered = 'Delivered'
choose_type = 'Choose type'
choose_lang = "Выберите язык"
added_to_card = '{} pieces {} added to cart'
finished_message = 'Finished'
proceed_to_order = 'Proceed to order'
send_location = 'Send your location'
checkout = 'Checkout'
remove_from_cart = 'Remove from cart'
confirm_order = 'Confirm'
not_confirm_order = 'Not confirm'
order_confirmed = 'Order confirmed'
order_not_confirmed = 'Order not confirmed'
order_succeed = 'Your order has been successfully placed!'
order_failed = 'Order failed'
order_canceled = 'Order canceled'
order_canceled_message = 'Your order has been canceled'
location = 'Location'
clear_cart = 'Clear cart'
final_order = """Final order {}
{}
{}
{} pieces {}
Final price: {} узс"""
payment_method = 'Payment method'
cash_payment = 'Cash'
card_payment = 'Card'
card_for_payment = 'Card for payment 9860260101234567'
accept_order = 'Accept order'
decline_order = 'Decline order'
order_accepted = 'Order accepted'
order_declined = 'Order declined'
order_accepted_message = 'Your order has been accepted'
order_declined_message = 'Your order has been declined'
send_order = 'Send order'
send_order_message = 'Your order has been sent'
order_done = 'Order done'
order_done_message = 'Your order has been done'

admin_text = {'2': 'Заказ принят ✅',
              '3': 'Заказ готов и отправлен 🚚',
              '4': 'Заказ выполнен ✅',
              '5': 'Заказ отменен ❌'
              }
user_status = {
    '2_ru': 'Заказ принят ✅',
    '3_ru': 'Заказ готов и отправлен 🚚',
    '4_ru': 'Приятного аппетита ☺️',
    '5_ru': 'Заказ отменен ❌',

    '2_uz': 'Buyurtma qabul qilindi ✅',
    '3_uz': 'Buyurtma tayyor va yetkazib berish uchun jo\'natildi 🚚',
    '4_uz': 'Yoqimli ishtaxa ☺️',
    '5_uz': 'Buyurtma bekor qilindi ❌'

}

messages = {
    'uz': {
        welcome: 'Xush kelibsiz 🤗',
        empty_cart: "Savatchangiz bo'sh 😧",
        lang_select: "Til o'zgardi ✅",
        feedback_succeed: "Fikr va mulohazalaringiz uchun rahmat 💭",
        feedback_send: "Quyida matn kiriting va jo\'nating",
        in_your_cart: "Savatchada:",
        your_orders: "Buyurtmalaringiz:",
        status: 'Holati',
        ordered: 'Buyurtma vaqti',
        delivered: 'Yetkazish vaqti',
        choose_type: 'Turini tanlang:',
        added_to_card: '{} dona {} savatchaga qo\'shildi',
        no_orders_yet: "Siz hanuz buyurtma qilmagansiz.",
        make_order_menu: '🛒 Buyurtma berish',
        cart_menu: '🛒 Savatcha',
        my_orders_menu: '🛍 Mening buyurtmalarim',
        language_menu: '🇺🇿 🇷🇺',
        feedback_menu: '✍️ Taklif bildirish',
        back_menu: 'Orqaga',
        proceed_to_order: 'Buyurtma berish',
        send_location: 'Lokatsiyani yuborish',
        finish_order_menu: 'Buyurtmani yakunlash',
        finished_message: 'Amalga oshirildi!',
        checkout: 'Buyurtmani tasdiqlash',
        clear_cart: 'Savatcha tozalash',
        confirm_order: 'Tasdiqlayman',
        not_confirm_order: 'Tasdiqlamayman',
        location: 'Lokatsiya',
        final_order: """Сизнинг буюртмангиз {}
{}  
{}
{}-та {}
Умумий толов(доставкасиз): {} узс""",
        payment_method: 'To\'lov usulini tanlang',
        cash_payment: 'Naqd 💵',
        card_payment: 'Karta 💳',
        send_order: 'Buyurtma yuborish',
        card_for_payment: 'Karta orqali to\'lov uchun 8600 1402 8764 0982 raqamiga Payme yoki Click ilova yordamida xaridni amalga oshirishing',
    },
    'ru': {
        welcome: 'Добро пожаловать!',
        empty_cart: "Ваша корзина пуста",
        lang_select: "Язык изменен",
        feedback_succeed: 'Спасибо за ваш отзыв!',
        feedback_send: "Введите текст ниже и отправьте.",
        in_your_cart: "В корзине:",
        your_orders: "Ваши заказы:",
        status: 'Состояние',
        ordered: 'Заказано',
        delivered: 'Доставлен',
        choose_type: 'Выберите тип:',
        added_to_card: '{} шт. {} добавлен в корзину',
        no_orders_yet: "Вы еще ничего не заказывали.",
        make_order_menu: '🛒 Сделать заказ',
        cart_menu: '🛒 Корзина',
        my_orders_menu: '🛍 Мои заказы',
        language_menu: '🇺🇿 🇷🇺',
        feedback_menu: '✍️ Обратная связь',
        back_menu: 'Назад',
        proceed_to_order: 'Оформить заказ',
        send_location: 'Отправить локацию',
        finish_order_menu: 'Завершить заказ',
        finished_message: 'Успешно!',
        checkout: 'Проверить заказ',
        clear_cart: 'Очистить корзину',
        confirm_order: 'Подтверждаю',
        not_confirm_order: 'Не подтверждаю',
        location: 'Локация',
        final_order: """ Ваш заказ {}
        {}
        {}
        {}-шт {}
        Сумма для оплаты(без доставки): {} узс
        """,
        accept_order: "Принять",
        decline_order: "Отклонить",
        payment_method: "Выберите способ оплаты",
        cash_payment: "Наличные 💵",
        card_payment: "На карту 💳",
        send_order: "Отправить заказ",
        card_for_payment: "Оплатите заказ с помощью приложения Payme или Click, переводя деньги на 8600 1402 8764 0982",

    },

}
