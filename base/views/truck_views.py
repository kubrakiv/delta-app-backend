from django.shortcuts import render, get_object_or_404
from django.db import transaction

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from rest_framework.response import Response
from rest_framework import status

from base.models import Truck
from base.serializers import TruckSerializer


# TRUCK VIEWS


@api_view(["GET"])
def getTrucks(request):
    trucks = Truck.objects.all()
    serializer = TruckSerializer(trucks, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def addTruck(request):
    data = request.data
    truck = Truck.objects.create(
        plates=data.get("plates"),
    )
    serializer = TruckSerializer(truck, many=False)
    return Response(serializer.data)
    