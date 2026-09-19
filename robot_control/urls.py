from django.urls import path
from . import views

app_name = 'robot_control'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/command/', views.proxy_command, name='proxy_command'),
]
