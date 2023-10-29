from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from .models import Task, Driver, Truck
from .serializers import TaskSerializer, DriverSerializer, TruckSerializer


# Create your views here.

@api_view(['GET'])
def getRoutes(request):
    return Response("Hello")

@api_view(['GET'])
def getTasks(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getTrucks(request):
    trucks = Truck.objects.all()
    serializer = TruckSerializer(trucks, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getTask(request, pk):
    task = Task.objects.get(id=pk)
    serializer = TaskSerializer(task, many=False)
    return Response(serializer.data)     


@api_view(['POST'])
def createTask(request):
    data = request.data
    print(data)
    driver_name = data.get('driver')
    truck_plate = data.get('truck')
    driver = Driver.objects.filter(full_name=driver_name).first()
    truck = Truck.objects.filter(plates=truck_plate).first()

    task = Task.objects.create(
        title=data.get('title'),
        start_date_time=data.get('start_date_time'),
        truck=truck,
        driver=driver
    )
    serializer = TaskSerializer(task, many=False)
    return Response(serializer.data)  


@api_view(['PUT'])
def editTask(request, pk):
    task = Task.objects.get(id=pk)
    serializer = TaskSerializer(instance=task, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)  


@api_view(['POST'])
def addDriver(request):
    data = request.data
    driver = Driver.objects.create(
        full_name=data.get('name'),
    )
    serializer = DriverSerializer(driver, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def addTruck(request):
    data = request.data
    truck = Truck.objects.create(
        plates=data.get('plates'),
    )
    serializer = TruckSerializer(truck, many=False)
    return Response(serializer.data)


