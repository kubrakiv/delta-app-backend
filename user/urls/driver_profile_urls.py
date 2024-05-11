from django.contrib import admin
from django.urls import path
from user.views import driver_profile_views as views


urlpatterns = [
    path("", views.getDriverProfiles, name="driver-profiles"),
    path("upload/", views.uploadDriverImage, name="driver-profile-image-upload"),
    path("update/<str:pk>/", views.updateDriverProfile, name="driver-profile-update"),
]