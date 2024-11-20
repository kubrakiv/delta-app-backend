from django.shortcuts import render, get_object_or_404
from django.db import transaction

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from rest_framework.response import Response
from rest_framework import status

from base.models import (
    Task,
    DriverProfile,
    Truck,
    Order,
    TaskType,
    Point,
)
from base.serializers import (
    TaskSerializer,
)


# TASKS VIEWS


@api_view(["GET"])
def getTasks(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getTask(request, pk):
    task = Task.objects.get(id=pk)
    serializer = TaskSerializer(task, many=False)
    return Response(serializer.data)


@api_view(["POST"])
def createTask(request):
    try:
        data = request.data
        print(data)

        driver_name = data.get("driver")
        truck_plate = data.get("truck")
        order_number = data.get("order")
        task_type_name = data.get("type")

        start_time = data.get("start_time")
        if start_time == "":
            start_time = None

        end_time = data.get("end_time")
        if end_time == "":
            end_time = None

        driver = DriverProfile.objects.filter(full_name=driver_name).first()
        truck = Truck.objects.filter(plates=truck_plate).first()
        task_type = TaskType.objects.filter(name=task_type_name).first()
        order = Order.objects.filter(number=order_number).first()
        point = Point.objects.filter(id=data.get("point_details", {}).get("id")).first()

        task = Task.objects.create(
            title=data.get("title"),
            start_date=data.get("start_date"),
            start_time=start_time,
            truck=truck,
            driver=driver,
            type=task_type,
            order=order,
            point=point,
        )
        serializer = TaskSerializer(task, many=False)
        return Response(serializer.data)
    except Exception as e:
        print(f"Error in createTask: {str(e)}")
        return Response({"error": "Error creating task"}, status=500)


@api_view(["PUT"])
def editTask(request, pk):
    task = Task.objects.get(id=pk)
    print(task)
    serializer = TaskSerializer(instance=task, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
    else: 
        print(serializer.errors)
    print(serializer.data)
    return Response(serializer.data)


@api_view(["DELETE"])
def deleteTask(request, pk):
    try:
        task = Task.objects.get(id=pk)
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = TaskSerializer(task, many=False)
    task.delete()

    return Response({"message": "Task deleted successfully", "data": serializer.data})

