from django.db import models
from django.core import serializers
import datetime


class Employee(models.Model):
    REGULAR = 'R'
    REGULAR1 = 'R1'
    PROBATION = 'P'

    employee_status_choices = [
        (REGULAR, 'Regular Employee'),
        (REGULAR1, 'Regular1 Employee'),
        (PROBATION, 'Probationary Employee')
    ]

    employee_tin_id = models.IntegerField(default=0, unique=True)
    name = models.CharField(max_length=200)
    probation_date = models.DateField()
    hired_date = models.DateField()
    sl_start_date = models.DateField()
    regularization_date = models.DateField()
    employee_status = models.CharField(max_length=2,
                                       choices=employee_status_choices,
                                       default=PROBATION)
    prev_vl_bal = models.FloatField(default=0.0)
    prev_sl_bal = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

    def get_total_leaves_taken(self):
        leaves_taken_obj_list = self.leave_set.all()
        sum_vl_taken = 0
        sum_sl_taken = 0

        for leaves_taken_obj in leaves_taken_obj_list:
            if leaves_taken_obj.type == "VL":
                sum_vl_taken += leaves_taken_obj.days
            elif leaves_taken_obj.type == "SL":
                sum_sl_taken += leaves_taken_obj.days

        return round(sum_vl_taken, 3), round(sum_sl_taken, 3)

    def get_earned_leaves(self):
        vl_list, sl_list = self.get_vl_sl_list()
        return zip(vl_list, sl_list)

    def get_leaves_taken(self):
        return serializers.serialize("json", self.leave_set.all())

    def get_offenses(self):
        return serializers.serialize("json", self.offense_set.all())

    def get_earned_vl_list(self):
        vl_list, sl_list = self.get_vl_sl_list()
        vl_list_serialized = serializers.serialize("json", vl_list)
        return vl_list_serialized

    def get_earned_sl_list(self):
        vl_list, sl_list = self.get_vl_sl_list()
        sl_list_serialized = serializers.serialize("json", sl_list)
        return sl_list_serialized

    def get_total_leaves(self):
        vl_list, sl_list = self.get_vl_sl_list()
        total_vl = self.prev_vl_bal
        total_sl = self.prev_sl_bal
        for vl in vl_list:
            total_vl += vl.value

        for sl in sl_list:
            total_sl += sl.value

        total_vl = round(total_vl, 3)
        total_sl = round(total_sl, 3)

        return total_vl, total_sl

    def get_vl_sl_list(self):
        emp_leaves = self.earnedleave_set.all()
        vl_list = []
        sl_list = []

        for leave in emp_leaves:
            if leave.type == 'VL':
                vl_list.append(leave)
            elif leave.type == 'SL':
                sl_list.append(leave)
        vl_list.sort(key=lambda x: x.cut_off)
        sl_list.sort(key=lambda x: x.cut_off)
        return vl_list, sl_list

    def get_timesheet_summary(self):
        emp_timesheet = self.timesheet_set.all()

        emp_timesheet_list = []
        for timesheet in emp_timesheet:
            if timesheet.time_in > datetime.time(hour=9, minute=0, second=0):
                late = 'YES'
            else:
                late = 'NO'

            if (timesheet.time_out - timesheet.time_in) < 8:
                ut = 'YES'
            else:
                ut = 'NO'

            emp_timesheet_list.append({'date': timesheet.date,
                                       'time_in': timesheet.time_in,
                                       'time_out': timesheet.time_out,
                                       'late': late,
                                       'ut': ut})
        return emp_timesheet_list


class Leave(models.Model):
    VL = 'VL'
    SL = 'SL'

    type_choices = [
        (VL, 'Vacation Leave'),
        (SL, 'Sick Leave')
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    days = models.FloatField(default=0.0)
    type = models.CharField(max_length=2,
                            choices=type_choices,
                            default=VL)


class Offense(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    offense_name = models.CharField(max_length=20)


class Earnedleave(models.Model):
    VL = 'VL'
    SL = 'SL'

    type_choices = [
        (VL, 'Vacation Leave'),
        (SL, 'Sick Leave')
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    cut_off = models.DateField()
    value = models.FloatField(default=0.0)
    type = models.CharField(max_length=2,
                            choices=type_choices,
                            default=VL)


class Timesheet(models.Model):

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    time_in = models.TimeField()
    time_out = models.TimeField()
    project = models.CharField(max_length=200)
