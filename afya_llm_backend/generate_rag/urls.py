from django.urls import path
from . import views

app_name = 'generate_rag'

urlpatterns = [
    path('', views.welcome_view, name='welcome'),
    path('rag/', views.rag_view, name='rag'),
] 