from django.urls import path
from . import views, apiViews

app_name = 'employee_profile'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.EmployeeDetailView.as_view(), name='employee_details'),
    path('save_changes', apiViews.save_changes, name='save_changes'),
    path('generate_leave_registry', apiViews.generate_leave_registry, name='generate_leave_registry'),
    path('download_file', apiViews.download_file, name='download_file'),
    path('add_employee', apiViews.add_employee, name='add_employee'),
    path('delete_employee', apiViews.delete_employee, name='delete_employee')
]
