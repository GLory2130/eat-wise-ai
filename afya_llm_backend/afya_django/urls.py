"""
URL configuration for afya_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def redirect_to_chatbot(request):
    return redirect('/chat/')

urlpatterns = [
    path('', redirect_to_chatbot, name='home'),
    path('admin/', admin.site.urls),
    path('chat/', include('frontend.urls')),
    path('afya/ml/', include('machine_learning.urls')),
    path('afya/intents/', include('intents.urls')),
    path('afya/rag/', include('generate_rag.urls')),
    # path('afya/', include('nutriapi.urls')),
]
