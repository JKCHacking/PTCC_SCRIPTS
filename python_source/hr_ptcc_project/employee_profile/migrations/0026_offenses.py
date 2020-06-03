# Generated by Django 3.0.6 on 2020-05-22 03:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employee_profile', '0025_auto_20200522_1114'),
    ]

    operations = [
        migrations.CreateModel(
            name='Offenses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('offense_name', models.CharField(max_length=10)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee_profile.Employee')),
            ],
        ),
    ]