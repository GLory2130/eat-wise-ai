from django.urls import path
from . import views

urlpatterns = [
    path('intents/', views.intents_view, name='intents'),
] 