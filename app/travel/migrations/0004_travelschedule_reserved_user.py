# Generated by Django 2.0.3 on 2018-04-11 03:56

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reservation', '0001_initial'),
        ('travel', '0003_auto_20180411_1131'),
    ]

    operations = [
        migrations.AddField(
            model_name='travelschedule',
            name='reserved_user',
            field=models.ManyToManyField(through='reservation.Reservation', to=settings.AUTH_USER_MODEL),
        ),
    ]
