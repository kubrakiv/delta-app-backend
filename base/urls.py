from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes, name="routes"),
    path('tasks/', views.getTasks, name="tasks"),
    path('trucks/', views.getTrucks, name="trucks"),
    path('tasks/<str:pk>', views.getTask, name="task"),
    path('tasks/create/', views.createTask, name="create-task"),
    path('drivers/add/', views.addDriver, name="add-driver"),
    path('trucks/add/', views.addTruck, name="add-truck"),
]
