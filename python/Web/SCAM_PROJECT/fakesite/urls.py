from django.urls import path
from. import views

urlpatterns = [
    path('', views.index, name='index'),
    path('error/', views.fake_error, name='error')
]
