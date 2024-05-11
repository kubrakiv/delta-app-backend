from django.contrib import admin
from django.urls import path
from base.views import customer_views as views

urlpatterns = [
    path("", views.getCustomers, name="customers")
]
