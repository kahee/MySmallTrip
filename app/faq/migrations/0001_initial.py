# Generated by Django 2.0.3 on 2018-04-06 08:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FrequentQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=30, verbose_name='주제')),
                ('subject2', models.CharField(blank=True, max_length=20, verbose_name='소주제')),
                ('question', models.TextField(verbose_name='질문')),
                ('answer', models.TextField(verbose_name='답변')),
                ('isusable', models.BooleanField(default=True, verbose_name='사용여부')),
                ('creationdatetime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='생성시간')),
                ('modifydatetime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='수정시간')),
            ],
        ),
    ]
