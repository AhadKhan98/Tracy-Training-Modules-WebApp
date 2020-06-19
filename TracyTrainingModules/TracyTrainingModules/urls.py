"""TracyTrainingModules URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from home_app import views as home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view.home, name='home'),
    path('home/', home_view.home, name='home'),
    path('login/',home_view.login,name='login'),
    path('register/',home_view.register,name='register'),
    path('section<int:sec_num>-module<int:module_num>/',home_view.module,name='module'),
    path('section<int:sec_num>-quiz/',home_view.quiz,name='quiz'),
    path('logout/',home_view.logout,name='logout'),
    path('section<int:sec_num>-success/',home_view.enable_next_section_and_redirect, name='enable_next_section_and_redirect'),
    path('completion/',home_view.completion,name='completion'),
]
