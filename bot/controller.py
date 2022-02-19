import json
import textwrap
from django.db.models import Sum, F, Q
import datetime
from bot import markups, constants
from bot.models import Command, Feedback
from product.models import Order, Product, CartItem, Category, AdminGroup, TelegramChat


def command_logging(user, message_id, text, from_menu=None, current_menu=None, to_menu=None,
                    category_id=None, update=False):
    if update:
        Command.objects.filter(message_id=message_id,
                               user=user).update(
            text=text,
            from_menu=from_menu,
            current_menu=current_menu,
            to_menu=to_menu,
            offset=offset,
            category_id=category_id,
            product=product)
    else:
        Command.objects.create(user=user,
                               message_id=message_id,
                               text=text,
                               from_menu=from_menu,
                               current_menu=current_menu,
                               to_menu=to_menu,
                               category_id=category_id)


class Controller:
    def __init__(self, bot, update, user, cart=None, last_command=None):
        self.bot = bot
        self.update = update
        self.user = user
        self.cart = cart
        self.last_command = last_command

    def get_lang(self):
        return self.user.language if self.user.language else 'ru'

    def start(self):
        self.bot.sendMessage(self.update.message.chat_id,
                             text=constants.messages[self.get_lang()][constants.welcome],
                             reply_markup=markups.home_markup(self.get_lang()))
        command_logging(user=self.user,
                        message_id=self.update.message.message_id,
                        text=self.update.message.text,
                        from_menu=constants.home,
                        to_menu=constants.home)

    def home_control(self):
        if self.update.message.text == constants.messages[self.get_lang()][constants.make_order_menu]:
            self.category_select()

        elif self.update.message.text == constants.messages[self.get_lang()][constants.cart_menu]:
            self.cart_check()

        elif self.update.message.text == constants.messages[self.get_lang()][constants.my_orders_menu]:
            self.order_history()

        elif self.update.message.text == constants.messages[self.get_lang()][constants.language_menu]:
            self.language_select()

        elif self.update.message.text == constants.messages[self.get_lang()][constants.feedback_menu]:
            self.feedback()

        # else:
        #     self.bot.sendMessage(self.update.message.chat_id, text='? in ?')

    def cart_check(self):
        cart_items = self.cart.all()
        if not cart_items.exists():
            self.bot.sendMessage(self.update.message.chat_id,
                                 text=constants.messages[self.get_lang()][constants.empty_cart],
                                 reply_markup=markups.home_markup(self.get_lang()))
            command_logging(user=self.user,
                            message_id=self.update.message.message_id,
                            text=self.update.message.text,
                            from_menu=constants.home,
                            current_menu=constants.home,
                            to_menu=constants.home)

        else:
            pcs = cart_items.values_list('quantity', flat=True)
            prods = cart_items.values_list('product__name', flat=True)
            zipped = zip(pcs, prods)

            items_str = ''
            for i, j in zipped:
                items_str += (str(i) + ' x ' + j + '\n')

            total = self.cart.aggregate(Total=Sum(F('price')))

            text = '{}\n{}\nTotal: {}'.format(constants.messages[self.get_lang()][constants.in_your_cart],
                                              items_str,
                                              total['Total'])

            self.bot.sendMessage(self.update.message.chat_id,
                                 text=text,
                                 reply_markup=markups.finish_order_markup(self.get_lang()))
            command_logging(user=self.user,
                            message_id=self.update.message.message_id,
                            text=self.update.message.text,
                            from_menu=constants.home,
                            current_menu=constants.proceed_to_order,
                            to_menu=constants.home)

    # create proceed order to get location
    def proceed_order(self):
        self.bot.sendMessage(self.update.message.chat_id,
                             text=constants.messages[self.get_lang()][constants.location],
                             reply_markup=markups.location_markup(self.get_lang()))
        command_logging(user=self.user,
                        message_id=self.update.message.message_id,
                        text=self.update.message.text,
                        from_menu=constants.home,
                        current_menu=constants.location,
                        to_menu=constants.home)

    def order_history(self):
        orders_history = Order.objects.filter(user=self.user)
        if orders_history.count() == 0:
            text = constants.messages[self.get_lang()][constants.no_orders_yet]
            self.bot.sendMessage(self.update.message.chat_id,
                                 text=text)
            command_logging(user=self.user,
                            message_id=self.update.message.message_id,
                            text=self.update.message.text,
                            from_menu=constants.home,
                            to_menu=constants.home)
        else:
            statuses = orders_history.values_list('status', flat=True)
            created_at = orders_history.values_list('created', flat=True)
            updated_at = orders_history.values_list('updated', flat=True)
            zipped = zip(statuses, created_at, updated_at)
            order_str = '{}:\n№.| {} \t | \t {} \t | \t {}\n'.format(
                constants.messages[self.get_lang()][constants.your_orders],
                constants.messages[self.get_lang()][constants.status],
                constants.messages[self.get_lang()][constants.ordered],
                constants.messages[self.get_lang()][constants.delivered],
            )
            counter = 1
            for i, j, k in zipped:
                order_str += '{}.| {} | {} | {}\n'.format(counter, i, j, k)
                counter += 1

            self.bot.sendMessage(self.update.message.chat_id,
                                 text=order_str)
            command_logging(user=self.user,
                            message_id=self.update.message.message_id,
                            text=self.update.message.text,
                            from_menu=constants.home,
                            to_menu=constants.home)

    def language_select(self):
        if self.last_command.to_menu == constants.language and \
                any(self.update.message.text in x for x in markups.languages):
            if self.update.message.text == '🇷🇺':
                self.user.language = 'ru'
            else:
                self.user.language = 'uz'
            self.user.save()

            text = constants.messages[self.get_lang()][constants.lang_select]

            self.bot.sendMessage(self.update.message.chat_id,
                                 text=text,
                                 reply_markup=markups.home_markup(self.get_lang()))
            command_logging(user=self.user,
                            message_id=self.update.message.message_id,
                            text=self.update.message.text,
                            from_menu=constants.home,
                            to_menu=constants.home)

        elif self.last_command.from_menu == constants.home:
            self.bot.sendMessage(self.update.message.chat_id,
                                 text=constants.messages[self.get_lang()][constants.choose_lang],
                                 reply_markup=markups.languages_markup)
            command_logging(user=self.user,
                            message_id=self.update.message.message_id,
                            text=self.update.message.text,
                            from_menu=constants.home,
                            to_menu=constants.language)

    def feedback(self):
        if self.last_command.current_menu == constants.feedback:
            Feedback.objects.create(user=self.user,
                                    text=self.update.message.text)
            text = constants.messages[self.get_lang()][constants.feedback_succeed]
            self.bot.sendMessage(self.update.message.chat_id,
                                 text=text,
                                 reply_markup=markups.home_markup(self.get_lang()))
            command_logging(user=self.user,
                            message_id=self.update.message.message_id,
                            text=self.update.message.text,
                            from_menu=constants.home,
                            to_menu=constants.home)

        elif self.last_command.from_menu == constants.home:
            text = constants.messages[self.get_lang()][constants.feedback_send]
            self.bot.sendMessage(self.update.message.chat_id,
                                 text=text,
                                 reply_markup=markups.back_markup(self.get_lang()))
            command_logging(user=self.user,
                            message_id=self.update.message.message_id,
                            text=self.update.message.text,
                            from_menu=constants.home,
                            current_menu=constants.feedback,
                            to_menu=constants.home)

    def go_home(self):
        self.bot.sendMessage(self.update.message.chat_id,
                             text=constants.messages[self.get_lang()][constants.welcome],
                             reply_markup=markups.home_markup(self.get_lang()))
        command_logging(user=self.user,
                        message_id=self.update.message.message_id,
                        text=self.update.message.text,
                        from_menu=constants.home,
                        to_menu=constants.home)

    def go_back(self):
        self.bot.sendMessage(self.update.message.chat_id,
                             text='Back',
                             reply_markup=markups.home_markup(self.get_lang()))
        command_logging(user=self.user,
                        message_id=self.update.message.message_id,
                        text=self.update.message.text,
                        from_menu=constants.home,
                        to_menu=constants.home)

    def add_to_card(self):
        command_logging(user=self.user,
                        message_id=self.update.message.message_id,
                        text=self.update.message.text,
                        from_menu=constants.home,
                        current_menu=constants.add_to_cart,
                        to_menu=constants.product)

        try:
            product = Product.objects.get(
                Q(name=self.last_command.text) |
                Q(name_en=self.last_command.text) |
                Q(name_ru=self.last_command.text)
            )
        except Product.DoesNotExist:
            product = None
            return self.bot.sendMessage(self.update.message.chat_id,
                                        text='Enter valid product',
                                        reply_markup=markups.categories_markup(self.get_lang()))

        quantity = int(self.update.message.text)

        if product and 0 < quantity <= 9:
            if (product.id,) in self.cart.values_list('product_id'):
                item = self.cart.get(product_id=product.id)
                item.quantity += quantity
                item.save()
            else:
                CartItem.objects.create(user=self.user, product=product, quantity=quantity)
        else:
            return self.bot.sendMessage(self.update.message.chat_id,
                                        text='Incorrect quantity {}'.format(
                                            self.update.message.text),
                                        reply_markup=markups.categories_markup(self.get_lang()))
        text = constants.messages[self.get_lang()][constants.added_to_card].format(
            self.update.message.text,
            self.last_command.text,
        )
        self.bot.sendMessage(self.update.message.chat_id,
                             text=text,
                             reply_markup=markups.categories_markup(self.get_lang()))

    def category_select(self):
        self.bot.sendMessage(self.update.message.chat_id,
                             text=constants.messages[self.get_lang()][constants.menu],
                             reply_markup=markups.categories_markup(self.get_lang()))
        command_logging(user=self.user,
                        message_id=self.update.message.message_id,
                        text=self.update.message.text,
                        from_menu=constants.home,
                        current_menu=constants.category,
                        to_menu=constants.product)

    def product_select(self):
        category = Category.objects.get(
            Q(name=self.update.message.text) |
            Q(name_en=self.update.message.text) |
            Q(name_ru=self.update.message.text)
        )
        query = Q(category_id=category.id, active_date=datetime.date.today())
        product = Product.objects.filter(query).last()
        markup = markups.pieces_markup(self.get_lang())
        text = f"*{product.name}*\n\n{product.description}\n{product.price} сум \n{product.active_date}"
        new_message = self.bot.sendPhoto(chat_id=self.update.message.chat_id,
                                         photo=str(product.photo_id),
                                         caption=text, parse_mode='Markdown', reply_markup=markup)
        command_logging(user=self.user,
                        message_id=new_message.message_id,
                        text=product.name,
                        from_menu=constants.category,
                        current_menu=constants.product,
                        to_menu=constants.add_to_cart,
                        category_id=category.id)

    def pieces_select(self):
        self.bot.sendMessage(self.update.message.chat_id,
                             text=self.update.message.text,
                             reply_markup=markups.pieces_markup(self.get_lang()))
        command_logging(user=self.user,
                        message_id=self.update.message.message_id,
                        text=self.update.message.text,
                        from_menu=constants.product,
                        current_menu=constants.pieces,
                        to_menu=constants.add_to_cart)

    def proceed_order(self):
        self.bot.sendMessage(self.update.message.chat_id,
                             text='Enter your phone number',
                             reply_markup=markups.categories_markup(self.get_lang()))
        command_logging(user=self.user,
                        message_id=self.update.message.message_id,
                        text=self.update.message.text,
                        from_menu=constants.home,
                        current_menu=constants.location,
                        to_menu=constants.phone_number)

    # create location handler with location markup
    def location(self):
        self.bot.sendMessage(self.update.message.chat_id,
                             text=constants.messages[self.get_lang()][constants.location],
                             reply_markup=markups.location_markup(self.get_lang()))
        command_logging(user=self.user,
                        message_id=self.update.message.message_id,
                        text=self.update.message.text,
                        from_menu=constants.home,
                        current_menu=constants.location,
                        to_menu=constants.checkout)

    # create checkout to confirm order
    def checkout(self):
        order = Order.objects.create(
            user=self.user,
            location=self.update.message.location.to_dict(),
        )
        order.cart.set(self.user.cart.filter(active=True))
        order.save()
        self.cart.all().update(active=False)
        self.bot.sendMessage(self.update.message.chat_id,
                             text=constants.messages[self.get_lang()][constants.payment_method],
                             reply_markup=markups.payment_markup(self.get_lang()))
        command_logging(user=self.user,
                        message_id=self.update.message.message_id,
                        text=self.update.message.text,
                        from_menu=constants.home,
                        current_menu=constants.checkout,
                        to_menu=constants.payment_method)

    # create confirm order handler
    def confirm_order(self):
        if self.update.message.text == constants.messages[self.get_lang()][constants.confirm_order]:
            self.bot.sendMessage(self.update.message.chat_id,
                                 text=constants.messages[self.get_lang()][constants.order_confirmed],
                                 reply_markup=markups.categories_markup(self.get_lang()))
            command_logging(user=self.user,
                            message_id=self.update.message.message_id,
                            text=self.update.message.text,
                            from_menu=constants.home,
                            current_menu=constants.confirm_order,
                            to_menu=constants.categories)
        else:
            self.bot.sendMessage(self.update.message.chat_id,
                                 text=constants.messages[self.get_lang()][constants.order_not_confirmed],
                                 reply_markup=markups.categories_markup(self.get_lang()))
            command_logging(user=self.user,
                            message_id=self.update.message.message_id,
                            text=self.update.message.text,
                            from_menu=constants.home,
                            current_menu=constants.confirm_order,
                            to_menu=constants.categories)

    def payment_method(self):
        if self.update.message.text == constants.messages[self.get_lang()][constants.card_payment]:
            payment = 1
        else:
            payment = 0

        order = Order.objects.filter(user=self.user, status=0, active=True).first()
        order.payment_type = payment
        order.save()
        text = textwrap.dedent(order.representate['text_' + self.get_lang()])
        if order.payment_type == 1:
            text += f'\n*{constants.messages[self.get_lang()][constants.card_for_payment]}*'
        self.bot.sendMessage(self.update.message.chat_id,
                             text=text,
                             parse_mode='Markdown',
                             reply_markup=markups.checkout_markup(self.get_lang()))
        command_logging(user=self.user,
                        message_id=self.update.message.message_id,
                        text=self.update.message.text,
                        from_menu=constants.checkout,
                        current_menu=constants.payment_method,
                        to_menu=constants.finish_order)

    def finish_order(self):
        if self.update.message.text == constants.messages[self.get_lang()][constants.confirm_order]:
            group = AdminGroup.objects.last()
            self.bot.sendMessage(chat_id=self.update.message.chat_id,
                                 text=constants.messages[self.get_lang()][constants.finished_message],
                                 reply_markup=markups.home_markup(self.get_lang()))
            order = Order.objects.filter(user=self.user, status=0, active=True).first()
            order.status = 1
            order.save()
            self.bot.sendLocation(chat_id=group.chat_id.telegram_id,
                                  longitude=order.location['longitude'],
                                  latitude=order.location['latitude']),
            self.bot.sendMessage(chat_id=group.chat_id.telegram_id,
                                 text=textwrap.dedent(order.representate['text_ru']),
                                 parse_mode='Markdown',
                                 reply_markup=markups.order_status_inline_markup(self.get_lang(), order.status,
                                                                                 order.id))

            command_logging(user=self.user,
                            message_id=self.update.message.message_id,
                            text=self.update.message.text,
                            from_menu=constants.finish_order,
                            to_menu=constants.home)

    # handler for changes status of order in admin panel with callback_query from inline_keyboard
    def change_status(self):
        order_id, action = self.update.callback_query.data.split(':')
        order = Order.objects.get(id=int(order_id))
        order.status = int(action)
        order.save()
        text = constants.admin_text[action]
        user_text = constants.user_status[action + '_' + self.get_lang()]
        self.bot.answerCallbackQuery(callback_query_id=self.update.callback_query.id,
                                     text=text,
                                     show_alert=True)
        self.bot.editMessageText(message_id=self.update.callback_query.message.message_id,
                                 chat_id=self.update.callback_query.message.chat_id,
                                 text=textwrap.dedent(order.representate['text_ru']),
                                 parse_mode='Markdown',
                                 reply_markup=markups.order_status_inline_markup(self.get_lang(), order.status,
                                                                                 order_id))
        self.bot.sendMessage(chat_id=order.user.telegram_id,
                             text=user_text,
                             parse_mode='Markdown')
