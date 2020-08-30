# Generated by Django 3.1 on 2020-08-30 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='URLtoUniqueCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.TextField(max_length=8192, verbose_name='url')),
                ('unique_code', models.TextField(unique=True, verbose_name='unique_code')),
                ('creation_time', models.DateTimeField(auto_now_add=True, verbose_name='creation_time')),
            ],
        ),
    ]