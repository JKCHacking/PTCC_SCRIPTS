# Generated by Django 3.0.6 on 2020-05-22 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_profile', '0027_auto_20200522_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offense',
            name='offense_name',
            field=models.CharField(choices=[('No Time-in', 'No Time-in'), ('No Time-out', 'No Time-out'), ('Late', 'Late')], max_length=20),
        ),
    ]