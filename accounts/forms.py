from django import forms
from django.contrib.auth import login, get_user_model
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import redirect

from accounts.models import Profile


class MyUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=200, required=True, validators=[validate_email])
    # first_name = forms.CharField(max_length=20, required=False)
    # last_name = forms.CharField(max_length=20, required=False)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2',
                  'first_name', 'last_name', 'email']
        field_classes = {'username': UsernameField}

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        if not first_name and not last_name:
            self.add_error("first_name", "Заполните имя или фамилию")
            self.add_error("last_name", "Заполните имя или фамилию")


    # class Meta:
    #     model = User
    #     fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email']


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']
        labels = {'first_name': 'Имя', 'last_name': 'Фамилия', 'email': 'Email'}

class ProfileChangeForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
