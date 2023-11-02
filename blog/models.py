from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    slug = models.CharField(max_length=150, verbose_name='slug', null=True, blank=True)
    body = models.TextField(verbose_name='Содержимое')
    image = models.ImageField(upload_to='blog/', null=True, blank=True, verbose_name='Превью')
    data_creation = models.DateTimeField(null=True, blank=True, verbose_name='Дата создания')

    views_count = models.IntegerField(default=0, verbose_name='Количество просмотров')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
