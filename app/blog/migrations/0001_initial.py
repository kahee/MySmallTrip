
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('reservation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('is_usable', models.BooleanField(default=True, verbose_name='사용여부')),
                ('creation_datetime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='생성시간')),
                ('modify_datetime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='수정시간')),
                ('travel_Reservation', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='reservation.Reservation')),
                ('title', models.CharField(max_length=100, verbose_name='후기제목')),
                ('Contents', models.TextField(blank=True, null=True, verbose_name='내용')),
                ('score', models.IntegerField(default=5, verbose_name='평점')),
            ],
            options={
                'ordering': ['-modify_datetime'],
            },
        ),
        migrations.CreateModel(
            name='BlogImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_usable', models.BooleanField(default=True, verbose_name='사용여부')),
                ('creation_datetime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='생성시간')),
                ('modify_datetime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='수정시간')),
                ('img_field', models.ImageField(upload_to='blog', verbose_name='후기 이미지')),
                ('blog_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Blog')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
