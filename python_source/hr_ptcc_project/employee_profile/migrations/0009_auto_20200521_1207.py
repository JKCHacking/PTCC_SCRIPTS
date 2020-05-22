# Generated by Django 3.0.6 on 2020-05-21 04:07

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('employee_profile', '0008_auto_20200521_1154'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employee',
            old_name='prev_leave_bal',
            new_name='prev_sl_bal',
        ),
        migrations.AddField(
            model_name='employee',
            name='prev_vl_bal',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='timesheet',
            name='date',
            field=models.DateTimeField(default=datetime.date(2020, 5, 21)),
        ),
        migrations.AlterField(
            model_name='leave',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 21, 4, 7, 44, 336125, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='timesheet',
            name='time_in',
            field=models.TimeField(default=datetime.time(4, 7, 44, 336125)),
        ),
        migrations.AlterField(
            model_name='timesheet',
            name='time_out',
            field=models.TimeField(default=datetime.time(4, 7, 44, 336125)),
        ),
    ]
