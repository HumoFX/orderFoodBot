from django.contrib import admin
from .models import Product, Order, Category, CartItem, AdminGroup, TelegramChat, Broadcast, BroadcastReceiver

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(AdminGroup)
admin.site.register(TelegramChat)
admin.site.register(Broadcast)
admin.site.register(BroadcastReceiver)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'created', 'updated', 'status']
    list_editable = ['status']

