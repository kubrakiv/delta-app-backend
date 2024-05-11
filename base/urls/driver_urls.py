from django.contrib import admin
from django.urls import path
from base.views import driver_views as views


urlpatterns = [
    path("", views.getDrivers, name="drivers"),
    path("add/", views.addDriver, name="add-driver"),
]
