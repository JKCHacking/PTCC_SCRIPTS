import datetime
from django.db import models
from django.utils import timezone


class Employee(models.Model):
    name = models.CharField(max_length=200)
    probation_date = models.DateTimeField()
    hired_date = models.DateTimeField()
    sl_start_date = models.DateTimeField()
    regularization_date = models.DateTimeField()
    employee_status = models.CharField(max_length=2)


class Leave(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.CharField(max_length=10)
    value = models.IntegerField(default=0)
    type = models.CharField(max_length=2)


class Timesheet(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    time_in = models.DateTimeField()
    time_out = models.DateTimeField()
    project = models.CharField(max_length=200)

