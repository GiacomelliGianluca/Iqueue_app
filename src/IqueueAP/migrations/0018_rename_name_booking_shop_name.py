# Generated by Django 4.2.1 on 2023-05-17 13:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('IqueueAP', '0017_booking'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='name',
            new_name='shop_name',
        ),
    ]
