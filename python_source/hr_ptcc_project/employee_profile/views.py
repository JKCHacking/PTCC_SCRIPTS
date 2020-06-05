import csv
import io
from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from .models import Employee, Leave, Earnedleave, Offense, Timesheet
from django.contrib.auth.decorators import permission_required
from django.http import JsonResponse
import logging
import dateutil.parser
import datetime
import calendar
logger = logging.getLogger(__name__)


class IndexView(generic.ListView):
    template_name = 'employee_profile/index.html'
    context_object_name = 'latest_employee_list'

    def get_queryset(self):
        query = self.request.GET.get('search')
        if query:
            object_list = Employee.objects.filter(name__icontains=query)
        else:
            object_list = Employee.objects.order_by('name')
        return object_list


class EmployeeDetailView(generic.DetailView):
    model = Employee
    template_name = 'employee_profile/employee_details.html'


@permission_required('admin.can_add_log_entry')
def upload_view(request):
    csv_file = request.FILES['file']
    csv_file_name = csv_file.name
    log_error = []
    message_header = 'Upload Done'

    if not csv_file_name.endswith('.csv'):
        return JsonResponse({"head": "Error", "body": "File must be CSV"})

    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)

    if csv_file_name == "employee.csv":
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            try:
                probation_date = (dateutil.parser.parse(column[2])).strftime("%Y-%m-%d")
                hired_date = (dateutil.parser.parse(column[3])).strftime("%Y-%m-%d")
                sl_start_date = (dateutil.parser.parse(column[4])).strftime("%Y-%m-%d")
                regularization_date = (dateutil.parser.parse(column[5])).strftime("%Y-%m-%d")

                _, created = Employee.objects.update_or_create(
                    employee_tin_id=column[0],
                    name=column[1],
                    probation_date=probation_date,
                    hired_date=hired_date,
                    sl_start_date=sl_start_date,
                    regularization_date=regularization_date,
                    employee_status=column[6],
                    prev_vl_bal=column[7],
                    prev_sl_bal=column[8],
                )
            except Exception as e:
                log_error.append(str(e))

        if log_error:
            message_body = f"[WARNING] There are errors found in your csv file: {log_error}"
        else:
            message_body = "All data has uploaded successfully"

    elif csv_file_name == "leaves.csv":
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            try:
                employee_tin_id = int(column[0])
                employee = Employee.objects.get(employee_tin_id=employee_tin_id)
                date_obj = (dateutil.parser.parse(column[2])).strftime("%Y-%m-%d")
                days = column[3]
                leave_type = column[4]

                _, created = Leave.objects.update_or_create(
                    employee=employee,
                    date=date_obj,
                    days=days,
                    type=leave_type
                )
            except Exception as e:
                log_error.append(str(e))

        if log_error:
            message_body = f"[WARNING] There are errors found in your csv file: {log_error}"
        else:
            message_body = "All data has uploaded successfully"

    elif csv_file_name == "offenses.csv":
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            try:
                employee_tin_id = int(column[0])
                employee = Employee.objects.get(employee_tin_id=employee_tin_id)
                date_obj = (dateutil.parser.parse(column[2])).strftime("%Y-%m-%d")
                offense_name = column[3]

                _, created = Offense.objects.update_or_create(
                    employee=employee,
                    date=date_obj,
                    offense_name=offense_name
                )
            except Exception as e:
                log_error.append(str(e))

        if log_error:
            message_body = f"[WARNING] There are errors found in your csv file: {log_error}"
        else:
            message_body = "All data has uploaded successfully"
    elif csv_file_name == "earned_leaves.csv":
        year_today = datetime.datetime.now().year

        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            try:
                employee_tin_id = int(column[0])
                employee = Employee.objects.get(employee_tin_id=employee_tin_id)
                leave_type = column[2]
                month_earned_list = [
                    column[3],
                    column[4],
                    column[5],
                    column[6],
                    column[7],
                    column[8],
                    column[9],
                    column[10],
                    column[11],
                    column[12],
                    column[13],
                    column[14]
                ]

                for i in range(len(month_earned_list)):
                    month_num = i + 1
                    first_cut_off_date = 15
                    second_cut_off_date = calendar.monthrange(year_today, month_num)[1]

                    first_cut_off = datetime.date(year_today, month_num, first_cut_off_date)
                    second_cut_off = datetime.date(year_today, month_num, second_cut_off_date)
                    value = round(float(month_earned_list[i]) / 2, 3)

                    _, created = Earnedleave.objects.update_or_create(
                        employee=employee,
                        cut_off=first_cut_off,
                        value=value,
                        type=leave_type
                    )
                    _, created = Earnedleave.objects.update_or_create(
                        employee=employee,
                        cut_off=second_cut_off,
                        value=value,
                        type=leave_type
                    )
            except Exception as e:
                log_error.append(str(e))

        if log_error:
            message_body = f"[WARNING] There are errors found in your csv file: {log_error}"
        else:
            message_body = "All data has uploaded successfully"
    else:
        message_header = 'Error'
        message_body = "You CSV File is Invalid"

    return JsonResponse({"head": message_header, "body": message_body})
