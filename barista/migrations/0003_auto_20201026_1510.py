# Generated by Django 3.1.2 on 2020-10-26 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barista', '0002_auto_20201026_1437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='email address'),
        ),
    ]
