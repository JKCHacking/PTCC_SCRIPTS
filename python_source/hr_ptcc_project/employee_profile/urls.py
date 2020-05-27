from django.urls import path
from . import views, apiViews

app_name = 'employee_profile'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.EmployeeDetailView.as_view(), name='employee_details'),
    path('save_employee', apiViews.save_employee, name='save_employee')
]
