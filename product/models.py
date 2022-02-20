import requests
import datetime
from django.db import models
from foodDelivery.local_settings import DJANGO_TELEGRAMBOT


class Category(models.Model):
    name = models.CharField(max_length=96)
    name_en = models.CharField(max_length=96, null=True, blank=True)
    name_ru = models.CharField(max_length=96, null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='subcategory', null=True, blank=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'


class Product(models.Model):
    name = models.CharField(max_length=96, null=True, blank=True)
    name_en = models.CharField(max_length=96, null=True, blank=True)
    name_ru = models.CharField(max_length=96, null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    available = models.BooleanField(default=True)
    photo = models.ImageField(upload_to='book/img/', null=True, blank=True)
    photo_id = models.CharField(max_length=256, verbose_name='Фото id в телеграм боте', null=True, blank=True)
    description = models.CharField(max_length=512, verbose_name='Описание', null=True, blank=True)
    description_en = models.CharField(max_length=512, verbose_name='Описание анг', null=True, blank=True)
    description_ru = models.CharField(max_length=512, verbose_name='Описание рус', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    active_date = models.DateField(verbose_name='Дата публикации')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')

    @property
    def active(self):
        if self.active_date <= datetime.date.today():
            return True

    def __str__(self):
        return '{} - {}'.format(self.category, self.name)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Product, self).save()
        print("update_fields", update_fields)
        chat_id = 996288857
        photo = {'photo': self.photo}
        token = DJANGO_TELEGRAMBOT['BOTS'][0]['TOKEN']
        data = {'chat_id': chat_id, 'caption': self.__str__()}
        url = f'https://api.telegram.org/bot{token}/sendPhoto'
        response = requests.post(url, data=data, files=photo)
        print(f"2 - {response.status_code}")
        if response.status_code != 200:
            raise ValidationError('Проблемы с файлом')
        else:
            self.photo_id = response.json()['result']['photo'][0]['file_id']

        return super(Product, self).save()


class Order(models.Model):
    STATUSES = (
        (0, 'Предзаказ'),
        (1, 'Новый'),
        (2, 'Готовка'),
        (3, 'Отправлен'),
        (4, 'Выполнен'),
        (5, 'Отменен'),
    )
    PAYMENT_TYPES = (
        (0, 'Наличные'),
        (1, 'На карту'),
    )
    user = models.ForeignKey('bot.TelegramUser', on_delete=models.CASCADE, related_name='orders')
    cart = models.ManyToManyField('CartItem')
    status = models.IntegerField(choices=STATUSES, default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    location = models.JSONField(max_length=256, null=True, blank=True)
    address = models.CharField(max_length=256, null=True, blank=True)
    comment = models.CharField(max_length=512, null=True, blank=True)
    payment_type = models.IntegerField(choices=PAYMENT_TYPES, default=0)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return '{}'.format(self.user.phone_number)

    @property
    def longitude(self):
        return self.location['longitude']

    @property
    def representate(self):
        cart_text = ''
        for product in self.cart.all():
            cart_text += product.__str__() + '\n'

        text_ru = f"""
        *Заказ №{self.id}*
        Cтатус: {self.get_status_display()}
        Дата: {self.created.strftime('%Y-%m-%d %H:%M')}
        Телефон: {self.user.phone_number}
        {cart_text}
        Способ оплаты: {self.get_payment_type_display()}
        
        *Стоимость: {self.cart.all().aggregate(models.Sum('price'))['price__sum']} сум*
        """
        text_uz = f"""
        *Buyurtma №{self.id}*
        Status: {self.get_status_display()}
        Sana: {self.created.strftime('%Y-%m-%d %H:%M')}
        Telefon: {self.user.phone_number}
        {cart_text}
        To`lov turi: {self.get_payment_type_display()}
        
        *Narxi: {self.cart.all().aggregate(models.Sum('price'))['price__sum']} sum*
        """
        return {"text_ru": text_ru, "text_uz": text_uz}

    # def order_date(self):
    #     return self.created.strftime('%B %d %Y')

    # def deliver_date(self):
    #     return self.updated.strftime('%B %d %Y')


class CartItem(models.Model):
    user = models.ForeignKey('bot.TelegramUser', on_delete=models.CASCADE, related_name='cart')
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.price = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return "{}x {}".format(self.quantity, self.product.category.name_ru)

    def representate(self, lang):
        if lang == 'uz':
            return f"{self.quantity}x {self.product.category.name}"
        else:
            return f"{self.quantity}x {self.product.category.name_ru}"


class TelegramChat(models.Model):
    """
    Represents a `chat` type in Bot API:
        https://core.telegram.org/bots/api#chat
    """
    CHAT_TYPES = (
        ("private", "private"),
        ("group", "group"),
        ("supergroup", "supergroup"),
        ("channel", "channel")
    )

    telegram_id = models.CharField(max_length=128, unique=True)
    type = models.CharField(choices=CHAT_TYPES, max_length=128)
    title = models.CharField(max_length=512, null=True, blank=True)
    username = models.CharField(max_length=128, null=True, blank=True)

    def is_private(self):
        return self.type == self.CHAT_TYPES[0][0]

    def __str__(self):
        return "{} - {} ({})".format(self.title, self.type, self.telegram_id)


class AdminGroup(models.Model):
    chat_id = models.ForeignKey(TelegramChat, on_delete=models.CASCADE, max_length=256, verbose_name='Чат id')
    name = models.CharField(max_length=256)
    users = models.ManyToManyField('bot.TelegramUser')

    def __str__(self):
        return self.name


class Text(models.Model):
    GROUP_TYPES = (
        (1, "Кнопка"),
        (2, "Сообщение")
    )

    field_name = models.CharField(max_length=128, unique=True)
    text_ru = models.CharField(max_length=512, null=True, blank=True)
    text_uz = models.CharField(max_length=512, null=True, blank=True)
    group = models.IntegerField(choices=GROUP_TYPES, default=1)

    def __str__(self):
        return self.text_ru
