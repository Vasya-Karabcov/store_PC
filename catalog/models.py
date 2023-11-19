from django.conf import settings
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=250, verbose_name='Наименование')
    description = models.CharField(max_length=550, verbose_name='Описание')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    name = models.CharField(max_length=250, verbose_name='Наименование')
    description = models.CharField(max_length=550, verbose_name='Описание')
    image = models.ImageField(upload_to='product/', null=True, blank=True, verbose_name='Превью')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    purchase_price = models.IntegerField(verbose_name='Цена за покупку')
    data_creation = models.DateTimeField(null=True, blank=True, verbose_name='Дата создания')
    last_data_modified = models.DateTimeField(null=True, blank=True, verbose_name='Дата последнего изменения')

    get_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Пользователь')

    def __str__(self):
        return f'{self.name}, {self.purchase_price} Руб.'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    num_vers = models.IntegerField(verbose_name='Номер версии')
    name_vers = models.CharField(max_length=150, verbose_name='Название версии')

    is_activ = models.BooleanField(default=True, verbose_name='Активна')

    def __str__(self):
        return f'{self.name_vers}'

    class Meta:
        verbose_name = 'Версия'
        verbose_name_plural = 'Версии'

