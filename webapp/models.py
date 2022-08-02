from django.db import models

CHOICE = [('other', 'разное'), ('bred', 'хлебо-булочные'), ('milk', 'молочка'), ('alco', 'алкоголь')]


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=2000, null=True, blank=True)
    category = models.TextField(max_length=30, choices=CHOICE, default=CHOICE[0][0])
    remain = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return f'Название:{self.name}'


class ProInBasket(models.Model):
    product = models.ForeignKey('webapp.Product', related_name='proinbaskets', on_delete=models.CASCADE,
                                verbose_name='Продукт')
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'Название:{self.product}'


class OrderBasket(models.Model):
    product = models.ForeignKey('webapp.Product', related_name='orderb', on_delete=models.CASCADE,
                                verbose_name='Продукт')
    quantity = models.PositiveIntegerField()
    order = models.ForeignKey('webapp.Order', related_name='orders', on_delete=models.CASCADE,
                              verbose_name='Заказ')


# class OrderProducts(models.Model):
#     order = models.ForeignKey('webapp.Order', on_delete=models.CASCADE, verbose_name='Заказ', related_name='orders')
#     product = models.ForeignKey('webapp.Product', related_name='orderb', on_delete=models.CASCADE,
#                                 verbose_name='Продукт')

class Order(models.Model):

    name = models.CharField(max_length=20, verbose_name='Имя')
    products = models.ManyToManyField('webapp.Product', related_name='orders', blank=True)
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    adres = models.CharField(max_length=60, verbose_name='Адрес')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def get_products(self):
        products = OrderBasket.objects.all()
        return products


