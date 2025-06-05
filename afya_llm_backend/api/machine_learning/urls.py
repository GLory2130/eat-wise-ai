from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome_view, name='welcome'),
    path('ml/', views.machine_learning_view, name='machine_learning'),
] 