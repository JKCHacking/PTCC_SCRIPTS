# Generated by Django 3.0.6 on 2020-05-21 01:04

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('employee_profile', '0004_auto_20200520_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leave',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 21, 1, 4, 52, 118465, tzinfo=utc)),
        ),
    ]
