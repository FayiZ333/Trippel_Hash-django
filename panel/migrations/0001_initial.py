# Generated by Django 3.2.7 on 2021-09-29 09:14

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='custom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=60, unique=True, verbose_name='email')),
                ('username', models.CharField(max_length=33, unique=True)),
                ('phone', models.CharField(max_length=10)),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('profile_img', models.ImageField(blank=True, default='fz/assain/img/fz.jpg', upload_to='fz/projects/img 1/user')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Catagory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat_name', models.CharField(max_length=333, unique=True)),
                ('cat_img', models.ImageField(blank=True, upload_to='fz/projects/img 1/prodect')),
                ('cat_slug', models.SlugField(max_length=303, unique=True)),
                ('cat_discription', models.TextField(blank=django.db.models.fields.TextField, max_length=333)),
                ('cat_date', models.CharField(max_length=333)),
            ],
        ),
        migrations.CreateModel(
            name='Prodect',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img1', models.ImageField(upload_to='fz/projects/img 1/prodect')),
                ('img2', models.ImageField(upload_to='fz/projects/img 1/prodect')),
                ('img3', models.ImageField(upload_to='fz/projects/img 1/prodect')),
                ('color', models.CharField(default='red', max_length=33)),
                ('brand', models.CharField(max_length=33)),
                ('prodectname', models.CharField(max_length=33)),
                ('gender', models.CharField(default='Men', max_length=33)),
                ('price', models.IntegerField()),
                ('model_no', models.CharField(max_length=33, unique=True)),
                ('stock', models.IntegerField(default=0)),
                ('slug', models.SlugField(max_length=303, unique=True)),
                ('discription', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('is_available', models.BooleanField(default=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('catagory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='panel.catagory')),
            ],
        ),
    ]
