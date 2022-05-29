from django import forms


class EmployeeForm(forms.Form):
    sl_start_date = forms.DateField()
    regularization_date = forms.DateField()
    employee_status = forms.CharField(max_length=2)

