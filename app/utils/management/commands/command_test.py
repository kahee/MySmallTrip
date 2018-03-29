from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from raven.contrib.django.raven_compat.models import client
# User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        try:
            2 / 0
        except ZeroDivisionError:
            client.captureException()




        #
        # if not User.objects.filter(username=settings.SUPERUSER_USERNAME).exists():
        #     User.objects.create_superuser(
        #         username=settings.SUPERUSER_USERNAME,
        #         password=settings.SUPERUSER_PASSWORD,
        #         email=settings.SUPERUSER_EMAIL
        #     )
