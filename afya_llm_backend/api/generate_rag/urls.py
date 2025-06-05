from django.urls import path
from . import views

urlpatterns = [
    path('rag/', views.rag_view, name='rag'),
] 