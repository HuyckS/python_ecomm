# Generated by Django 2.2.4 on 2020-12-23 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_ecomm', '0003_order_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total',
            field=models.IntegerField(),
        ),
    ]
