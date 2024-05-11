from django.contrib import admin
from django.urls import path
from base.views import truck_views as views


urlpatterns = [
    path("", views.getTrucks, name="trucks"),
    path("add/", views.addTruck, name="add-truck"),
]
