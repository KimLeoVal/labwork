from pyexpat import model

from django import forms
from django.forms import widgets

from webapp.models import Product, Order


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

# class SearchForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = ['name']

class SearchForm(forms.Form):
    search = forms.CharField(max_length=50, required=False, label='Найти')

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ['products']

class AddQtyToBasketForm(forms.Form):
    qty = forms.IntegerField(label="Укажите нужное количество")
