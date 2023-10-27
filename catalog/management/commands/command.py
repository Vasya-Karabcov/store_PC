from django.core.management import BaseCommand

from catalog.models import Category


class Command(BaseCommand):

    def handle(self, *args, **options):
        category_list = [
            {'name': 'Оперативная память', 'description': 'Все виды оперативной памяти'},
            {'name': 'Блоки питания', 'description': 'Все виды блоков питания'},
            {'name': 'Система охлаждения', 'description': 'Все виды охлаждения ПК'},
        ]

        for category_item in category_list:
            Category.objects.create(**category_item)
