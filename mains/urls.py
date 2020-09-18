"""this module holds the mains app urls"""

from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
] 