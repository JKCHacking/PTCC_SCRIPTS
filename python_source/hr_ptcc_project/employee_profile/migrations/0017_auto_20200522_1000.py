# Generated by Django 3.0.6 on 2020-05-22 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_profile', '0016_auto_20200522_0957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='earnedleave',
            name='cut_off',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='hired_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='probation_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='regularization_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='sl_start_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='leave',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='timesheet',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='timesheet',
            name='time_in',
            field=models.TimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='timesheet',
            name='time_out',
            field=models.TimeField(auto_now_add=True),
        ),
    ]
