# Generated by Django 3.0.6 on 2020-05-27 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_profile', '0028_auto_20200522_1151'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='employee_tin_id',
            field=models.IntegerField(default=0),
        ),
    ]
