# Generated by Django 3.0.6 on 2020-05-22 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_profile', '0019_auto_20200522_1011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='probation_date',
            field=models.DateTimeField(),
        ),
    ]
