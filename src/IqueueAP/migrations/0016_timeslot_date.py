# Generated by Django 4.2.1 on 2023-05-16 16:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("IqueueAP", "0015_remove_shop_coordinates_shop_lat_shop_lon_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="timeslot",
            name="date",
            field=models.DateField(default=datetime.date.today),
        ),
    ]
