from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from .models import Employee


class IndexView(generic.ListView):
    template_name = 'employee_profile/index.html'
    context_object_name = 'latest_employee_list'

    def get_queryset(self):
        return Employee.objects.order_by('name')


class EmployeeDetailView(generic.DetailView):
    model = Employee
    template_name = 'employee_profile/employee_details.html'