# Generated by Django 4.2.1 on 2023-05-08 15:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('IqueueAP', '0003_alter_shop_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shop',
            name='number_of_ratings',
        ),
        migrations.RemoveField(
            model_name='shop',
            name='queue',
        ),
        migrations.RemoveField(
            model_name='shop',
            name='rating',
        ),
    ]
