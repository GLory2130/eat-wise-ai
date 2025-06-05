from django.urls import path
from . import views

app_name = 'machine_learning'

urlpatterns = [
    path('', views.machine_learning_view, name='chat'),
] 