from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='DackZi26@yandex.ru',
            first_name='Boss',
            last_name='Bossov',
            is_superuser=True,
            is_staff=True,
            is_active=True
        )

        user.set_password('658311')
        user.save()