# Generated by Django 3.0.6 on 2020-05-22 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_profile', '0020_auto_20200522_1012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='earnedleave',
            name='cut_off',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='employee',
            name='hired_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='employee',
            name='probation_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='employee',
            name='regularization_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='employee',
            name='sl_start_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='leave',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='timesheet',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='timesheet',
            name='time_in',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='timesheet',
            name='time_out',
            field=models.TimeField(),
        ),
    ]
