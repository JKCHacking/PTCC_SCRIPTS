from django.contrib import admin
from .models import Employee, Leave, Timesheet, Earnedleave, Offense

admin.site.register(Employee)
admin.site.register(Leave)
admin.site.register(Earnedleave)
admin.site.register(Timesheet)
admin.site.register(Offense)
