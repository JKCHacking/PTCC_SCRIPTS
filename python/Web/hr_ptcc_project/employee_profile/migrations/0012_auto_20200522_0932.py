# Generated by Django 3.0.6 on 2020-05-22 01:32

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('employee_profile', '0011_auto_20200521_1209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leave',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 5, 22, 1, 32, 58, 812463, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='timesheet',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 5, 22, 1, 32, 58, 814483, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='timesheet',
            name='time_in',
            field=models.TimeField(default=datetime.datetime(2020, 5, 22, 1, 32, 58, 814483, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='timesheet',
            name='time_out',
            field=models.TimeField(default=datetime.datetime(2020, 5, 22, 1, 32, 58, 814483, tzinfo=utc)),
        ),
        migrations.CreateModel(
            name='Earnedleave',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cut_off', models.DateField(default=datetime.datetime(2020, 5, 22, 1, 32, 58, 814483, tzinfo=utc))),
                ('value', models.IntegerField(default=0)),
                ('type', models.CharField(choices=[('VL', 'Vacation Leave'), ('SL', 'Sick Leave')], default='VL', max_length=2)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee_profile.Employee')),
            ],
        ),
    ]