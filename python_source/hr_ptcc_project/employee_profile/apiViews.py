from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from openpyxl import load_workbook
from .models import Employee, Earnedleave, Leave, Offense
# import the logging library
import logging
import dateutil.parser
import json
import os
import datetime

# Get an instance of a logger
logger = logging.getLogger(__name__)


@csrf_exempt
def save_employee(request):
    data = request.POST.get('data', '')
    data_dict = json.loads(data)
    log_error = []

    for edited_employee_data in data_dict:
        id = data_dict[edited_employee_data]['id']
        type = data_dict[edited_employee_data]['type']
        value = data_dict[edited_employee_data]['value']

        model_parts = type.split('-')
        table_name = model_parts[0]
        column_name = model_parts[1]

        if table_name == "employee":
            try:
                employee = Employee.objects.get(id=id)
            except Employee.DoesNotExist:
                log_error.append(f"Employee with ID {id} does not exist!")

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

        if table_name == "earned":
            try:
                earned_leave_model = Earnedleave.objects.get(id=id)
            except Earnedleave.DoesNotExist:
                log_error.append(f"Earned Leave with ID {id} does not exist!")

            earned_leave_model.value = value
            earned_leave_model.save()

        if table_name == "leave":
            try:
                leave_model = Leave.objects.get(id=id)
            except Leave.DoesNotExist:
                log_error.append(f"Leave with ID {id} does not exist!")

            if column_name == "date":
                date_obj = dateutil.parser.parse(value)
                leave_model.date = date_obj

            if column_name == "days":
                leave_model.days = value

            if column_name == "type":
                leave_model.type = value

            leave_model.save()

        if table_name == "offense":
            try:
                offense_model = Offense.objects.get(id=id)
            except Offense.DoesNotExist:
                log_error.append(f"Offense Object with ID {id} does not exist!")

            if column_name == "date":
                date_obj = dateutil.parser.parse(value)
                offense_model.date = date_obj

            if column_name == "offense_name":
                offense_model.offense_name = value

            offense_model.save()

    if len(log_error) == len(data_dict):
        header_message = "Error"
        body_message = f"Changes cannot be made reason: {log_error}"
    elif log_error and len(log_error) < len(data_dict):
        header_message = "Warning"
        body_message = f"There are some changes failed to save: {log_error}"
    else:
        header_message = "Success"
        body_message = "All changes has been saved!"
    return JsonResponse({"head": header_message, "body": body_message})

@csrf_exempt
def generate_leave_registry(request):
    header_message = ""
    body_message = ""
    employee_id_list = request.POST.getlist('checked_employees[]')
    year = request.POST.get('year')

    template_ss_path = os.path.join(settings.STATIC_ROOT, 'employee_profile', 'files',
                                    'leave_registry_template_v1.xlsx')
    generated_file_path = os.path.join(settings.STATIC_ROOT, 'employee_profile', 'files',
                                       f'generated_leave_registry_{year}.xlsx')

    workbook = load_workbook(filename=template_ss_path)

    for id_string in employee_id_list:
        id_int = int(id_string)
        employee_object = Employee.objects.get(id=id_int)
        template_work_sheet = workbook.worksheets[0]
        emp_reg_ws = workbook.copy_worksheet(template_work_sheet)

        employee_name = employee_object.name
        hired_date = employee_object.hired_date
        regular_date = employee_object.regularization_date
        employee_status = employee_object.employee_status

        vacation_leave_benefits = 0
        sick_leave_benefits = 0
        if employee_status == "R":
            vacation_leave_benefits = 15
            sick_leave_benefits = 10
        elif employee_status == "R1":
            vacation_leave_benefits = 10
            sick_leave_benefits = 10
        elif employee_status == "P":
            vacation_leave_benefits = 0
            sick_leave_benefits = 10
        date_today = datetime.datetime.now().date()
        vl_balance = employee_object.prev_vl_bal
        sl_balance = employee_object.prev_sl_bal

        # employee details section
        emp_reg_ws['G3'] = employee_name
        emp_reg_ws['G4'] = hired_date.strftime('%B %d, %Y')
        emp_reg_ws['G5'] = regular_date.strftime('%B %d, %Y')
        emp_reg_ws['G6'] = vacation_leave_benefits
        emp_reg_ws['G7'] = sick_leave_benefits
        emp_reg_ws['G8'] = date_today.strftime('%B %d, %Y')

        # earned leave credits section
        emp_reg_ws['C11'] = year
        emp_reg_ws['C15'] = vl_balance
        emp_reg_ws['D15'] = sl_balance

        count = 16
        total_earned_vl = 0
        total_earned_sl = 0
        for vl, sl in employee_object.get_earned_leaves():
            if str(vl.cut_off.year) == year and str(sl.cut_off.year) == year:
                vl_value = vl.value
                sl_value = sl.value
                vl_cell_name = f'C{count}'
                sl_cell_name = f'D{count}'
                emp_reg_ws[vl_cell_name] = vl_value
                emp_reg_ws[sl_cell_name] = sl_value

                total_earned_vl += vl_value
                total_earned_sl += sl_value
                count += 1
        emp_reg_ws['C40'] = total_earned_vl
        emp_reg_ws['D40'] = total_earned_sl

        # details of leave taken
        
        total_vl_taken = 0
        total_sl_taken = 0
        for taken_leave_obj in employee_object.leave_set.all():
            if str(taken_leave_obj.date.year) == year:
                if taken_leave_obj.type == 'VL':
                    total_vl_taken += taken_leave_obj.days
                elif taken_leave_obj.type == 'SL':
                    total_sl_taken += taken_leave_obj.days

        # summary of leaves taken
        emp_reg_ws['G10'] = date_today.strftime('%B %d, %Y')
        emp_reg_ws['G13'] = total_earned_vl
        emp_reg_ws['G14'] = total_earned_sl
        emp_reg_ws['H13'] = total_vl_taken
        emp_reg_ws['H14'] = total_sl_taken
        emp_reg_ws['I13'] = total_earned_vl - total_vl_taken
        emp_reg_ws['I14'] = total_earned_sl - total_sl_taken
        emp_reg_ws.title = f'{employee_object.name}_{year}_leave_registry'

    workbook.save(generated_file_path)
    return JsonResponse({"head": header_message, "body": body_message})
