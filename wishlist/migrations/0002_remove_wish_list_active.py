# Generated by Django 3.2.8 on 2021-11-09 03:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wishlist', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wish_list',
            name='active',
        ),
    ]
