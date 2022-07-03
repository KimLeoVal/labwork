from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=2000, null=True,blank=True)
    category = models.Choices()


