from django.contrib import admin

from webapp.models import Product, ProInBasket, Order, OrderBasket

admin.site.register(Product)
admin.site.register(ProInBasket)
admin.site.register(Order)
admin.site.register(OrderBasket)
