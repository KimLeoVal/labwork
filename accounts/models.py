from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.

class Profile(models.Model):
    avatar =models.ImageField(upload_to='avatars',null=True,blank=True,verbose_name='Аватар')
    git=models.URLField(max_length=100,blank=True,null=True,verbose_name='Ссылка')
    about = models.TextField(max_length=2000,null=True,blank=True,verbose_name='О себе')
    user =models.OneToOneField(get_user_model(),on_delete=models.CASCADE,related_name='profile',verbose_name='Пользователь')
