from django.shortcuts import render, get_object_or_404
from django.db import transaction

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from rest_framework.response import Response
from rest_framework import status

from base.models import Truck, Trailer, DriverProfile
from base.serializers import TruckSerializer


# TRUCK VIEWS


@api_view(["GET"])
def getTrucks(request):
    trucks = Truck.objects.all()
    serializer = TruckSerializer(trucks, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def createTruck(request):
    data = request.data

    end_date = data.get("end_date")
    if end_date == "":
        end_date = None

    entry_date = data.get("entry_date")
    if entry_date == "":
        entry_date = None
    
    year = data.get("year")
    if year == "":
        year = None

    # Convert price to an integer
    price = int(float(data.get("price"))) if data.get("price") else None

    truck = Truck.objects.create(
        brand=data.get("brand"),
        model=data.get("model"),
        plates=data.get("plates"),
        vin_code=data.get("vin_code"),
        year=year,
        entry_date=entry_date,
        end_date=end_date,
        entry_mileage=data.get("entry_mileage"),
        price=price,
    )
    serializer = TruckSerializer(truck, many=False)
    return Response(serializer.data)


@api_view(["DELETE"])
def deleteTruck(request, pk):
    try:
        truck = Truck.objects.get(id=pk)
    except Truck.DoesNotExist:
        return Response("Truck does not exist", status=status.HTTP_404_NOT_FOUND)
    
    # Serialize the truck before deleting
    serializer = TruckSerializer(truck, many=False)
    truck.delete()

    return Response({"message": "Truck deleted"})


@api_view(["PUT"])
def updateTruckTrailerAndDriver(request, pk):
    data = request.data
    print("TRUCK DATA", data)
    try:
        # Get the truck instance
        truck = Truck.objects.get(id=pk)
    except Truck.DoesNotExist:
        return Response({"error": "Truck not found"}, status=404)

    # Extract trailer and driver information from request data
    trailer_plates = request.data.get("trailer")
    driver_name = request.data.get("driver")

    # Update the trailer if trailer plates are provided
    if trailer_plates:
        try:
            trailer = Trailer.objects.get(plates=trailer_plates)
            truck.trailer = trailer
        except Trailer.DoesNotExist:
            return Response({"error": "Trailer not found"}, status=404)

    # Update the driver if driver name is provided
    if driver_name:
        try:
            driver = DriverProfile.objects.get(full_name=driver_name)
            truck.driver = driver
        except DriverProfile.DoesNotExist:
            return Response({"error": "Driver not found"}, status=404)

    # Save the truck instance with the updated data
    truck.save()

    # Serialize the updated truck data and return it
    serializer = TruckSerializer(instance=truck, partial=True)
    return Response(serializer.data)

@api_view(["PUT"])
def updateTruck(request, pk):
    try:
        truck = Truck.objects.get(id=pk)
    except Truck.DoesNotExist:
        return Response({"error": "Truck not found"}, status=404)

    data = request.data

    end_date = data.get("end_date")
    if end_date == "":
        end_date = None

    entry_date = data.get("entry_date")
    if entry_date == "":
        entry_date = None

    # Convert price to an integer
    price = int(float(data.get("price"))) if data.get("price") else None

    truck.brand = data.get("brand")
    truck.model = data.get("model")
    truck.plates = data.get("plates")
    truck.vin_code = data.get("vin_code")
    truck.year = data.get("year")
    truck.entry_date = entry_date
    truck.end_date = end_date
    truck.entry_mileage = data.get("entry_mileage")
    truck.price = price

    truck.save()
    serializer = TruckSerializer(instance=truck, partial=True)
    return Response(serializer.data)

    