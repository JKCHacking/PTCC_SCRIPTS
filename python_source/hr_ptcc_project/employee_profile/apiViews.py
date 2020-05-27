from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Employee, Earnedleave
# import the logging library
import logging
import dateutil.parser
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


@csrf_exempt
def save_employee(request):
    data = request.POST.get('data', '')
    data_dict = json.loads(data)

    for edited_employee_data in data_dict:
        id = data_dict[edited_employee_data]['id']
        type = data_dict[edited_employee_data]['type']
        value = data_dict[edited_employee_data]['value']

        model_parts = type.split('-')
        table_name = model_parts[0]
        column_name = model_parts[1]

        if table_name == "earned":
            earned_leave_model = Earnedleave.objects.get(id=id)
            earned_leave_model.value = value

            earned_leave_model.save()

        if table_name == "employee":
            employee = Employee.objects.get(id=id)

            if column_name == "regularization_date":
                date_obj = dateutil.parser.parse(value)
                employee.regularization_date = date_obj

            if column_name == "employee_status":
                employee.employee_status = value

            if column_name == "prev_vl_bal":
                employee.prev_vl_bal = value

            if column_name == "prev_sl_bal":
                employee.prev_sl_bal = value

            employee.save()

    return JsonResponse({"success": "All changes has been saved!"})
