import csv
import io
from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from .models import Employee
from django.contrib.auth.decorators import permission_required
from django.http import JsonResponse
import logging
import dateutil.parser
logger = logging.getLogger(__name__)

class IndexView(generic.ListView):
    template_name = 'employee_profile/index.html'
    context_object_name = 'latest_employee_list'

    def get_queryset(self):
        return Employee.objects.order_by('name')


class EmployeeDetailView(generic.DetailView):
    model = Employee
    template_name = 'employee_profile/employee_details.html'


@permission_required('admin.can_add_log_entry')
def upload_view(request):
    csv_file = request.FILES['file']
    csv_file_name = csv_file.name

    if not csv_file_name.endswith('.csv'):
        return JsonResponse({"head": "Error", "body": "File must be CSV"})

    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)

    if csv_file_name == "employee.csv":
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
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
        return JsonResponse({"head": "Success", "body": "Upload Successfully!"})
    elif csv_file_name == "leaves.csv":
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
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
        return JsonResponse({"head": "Success", "body": "Upload Successfully!"})
