# Generated by Django 2.2.4 on 2020-12-23 07:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_ecomm', '0004_auto_20201222_2311'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='total',
        ),
    ]
