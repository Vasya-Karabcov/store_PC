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

    def __str__(self):
        return f'{self.name}, {self.purchase_price}'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
