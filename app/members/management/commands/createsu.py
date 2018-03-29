from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

User = get_user_model()


# class Command(BaseCommand):
#     def handle(self, *args, **options):
#         if not User.objects.filter(username=settings.SUPERUSER_USERNAME).exists():
#             User.objects.create_superuser(
#                 username=settings.SUPERUSER_USERNAME,
#                 password=settings.SUPERUSER_PASSWORD,
#                 email=settings.SUPERUSER_EMAIL
#             )
class Command(BaseCommand):
    def handle(self, *args, **kwargs):
         if not User.objects.filter(username=settings.SECRETS['SUPERUSER_USERNAME']).exists():
            User.objects.create_superuser(
                username=settings.SECRETS['SUPERUSER_USERNAME'],
                password=settings.SECRETS['SUPERUSER_PASSWORD'],
                email=settings.SECRETS['SUPERUSER_EMAIL'],
            )