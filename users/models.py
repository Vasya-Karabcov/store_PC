
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='Email')

    avatar = models.ImageField(upload_to='users/', null=True, blank=True, verbose_name='Аватар')
    phone = models.CharField(max_length=35, verbose_name='Номер телефона', blank=True, null=True)
    contry = models.CharField(max_length=90, verbose_name='Страна', null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []