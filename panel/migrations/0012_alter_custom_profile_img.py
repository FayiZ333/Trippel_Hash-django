# Generated by Django 3.2.8 on 2021-11-04 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0011_auto_20211029_1112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='custom',
            name='profile_img',
            field=models.ImageField(blank=True, null=True, upload_to='profile'),
        ),
    ]
