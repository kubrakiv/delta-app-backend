from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.middleware.csrf import get_token
from django.http import JsonResponse
from django.db import transaction

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from user.models import DriverProfile
from user.serializers import DriverProfileSerializer

from django.contrib.auth.hashers import make_password
from rest_framework import status


@api_view(["GET"])
def getDriverProfiles(request):
    drivers = DriverProfile.objects.all()
    serializer = DriverProfileSerializer(drivers, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def getDriverProfile(request, pk):
    driver = DriverProfile.objects.get(user=pk)
    serializer = DriverProfileSerializer(driver, many=False)
    return Response(serializer.data)


@api_view(["PUT"])
def updateDriverProfile(request, pk):
    driver = DriverProfile.objects.get(user=pk)
    serializer = DriverProfileSerializer(instance=driver, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(["POST"])
def uploadDriverImage(request):
    data = request.data

    driver_id = data["driver_id"]
    driver = DriverProfile.objects.get(user=driver_id)
    driver.image = request.FILES.get("image")
    driver.save()

    # Get the URL of the uploaded image
    image_url = request.build_absolute_uri(driver.image.url)

    # Return the URL of the uploaded image in the response
    return Response({"image_url": image_url}, status=status.HTTP_201_CREATED)

@api_view(["POST"])
def createDriverProfile(request):
    data = request.data
    driver = DriverProfile.objects.create(
        user_id=data["user"],
        image="default.jpg",
        license_number=data["license_number"],
        license_expiry_date=data["license_expiry_date"],
        license_image="default.jpg",
        truck_id=data["truck"],
        truck_image="default.jpg",
        truck_license_number=data["truck_license_number"],
        truck_license_expiry_date=data["truck_license_expiry_date"],
        truck_license_image="default.jpg",
        is_verified=False
    )

    serializer = DriverProfileSerializer(driver, many=False)
    return Response(serializer.data)

@api_view(["DELETE"])
def deleteDriverProfile(request, pk):
    driver = DriverProfile.objects.get(user=pk)
    driver.delete()
    return Response("Driver Profile Deleted Successfully")


