# Generated by Django 4.2.1 on 2023-05-11 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IqueueAP', '0007_remove_account_account_id_timeslot_shop'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='category',
            field=models.CharField(default='Others', max_length=100),
        ),
    ]
