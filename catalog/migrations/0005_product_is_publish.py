# Generated by Django 4.2.6 on 2023-11-22 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_product_get_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_publish',
            field=models.BooleanField(default=False, verbose_name='Опубликовано'),
        ),
    ]
