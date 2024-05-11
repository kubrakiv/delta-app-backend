from django.shortcuts import render, get_object_or_404
from django.db import transaction

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from rest_framework.response import Response
from rest_framework import status

from base.models import Driver
from base.serializers import DriverSerializer


# DRIVER VIEWS


@api_view(["GET"])
def getDrivers(request):
    drivers = Driver.objects.all()
    serializer = DriverSerializer(drivers, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def addDriver(request):
    data = request.data
    driver = Driver.objects.create(
        full_name=data.get("name"),
    )
    serializer = DriverSerializer(driver, many=False)
    return Response(serializer.data)
    