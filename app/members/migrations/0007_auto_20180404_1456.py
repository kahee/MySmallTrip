# Generated by Django 2.0.3 on 2018-04-04 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0006_auto_20180403_1511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='mypoint',
            field=models.IntegerField(blank=True, verbose_name='내포인트'),
        ),
    ]
