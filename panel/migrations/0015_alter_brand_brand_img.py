# Generated by Django 3.2.8 on 2021-11-07 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0014_alter_brand_brand_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='brand_img',
            field=models.ImageField(blank=True, upload_to='fz/projects/img 1/brand'),
        ),
    ]
