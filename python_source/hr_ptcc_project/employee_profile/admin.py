from django.contrib import admin
from .models import Employee, Leave, Timesheet

admin.site.register(Employee)
admin.site.register(Leave)
admin.site.register(Timesheet)
