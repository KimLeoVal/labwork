from django.contrib import admin

from webapp.models import Product,  Order, OrderBasket


class OrderBasketInline(admin.TabularInline):
    model = OrderBasket



class OrderAdmin(admin.ModelAdmin):
    def get_products(self):
        products = OrderBasket.objects.all()
        return products

    inlines = [
        OrderBasketInline,
    ]
    list_display = ['id', 'name', 'phone', 'created_at',]
    ordering = ['-created_at']
    fields = [ 'name', 'phone','adres']



admin.site.register(Product)

admin.site.register(Order,OrderAdmin)
admin.site.register(OrderBasket)

