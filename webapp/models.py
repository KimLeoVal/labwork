
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