from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task, Driver, Truck


class TaskSerializer(serializers.ModelSerializer):
    # user = serializers.CharField(source="user.username")
    truck = serializers.CharField(source="truck.plates")
    driver = serializers.CharField(source="driver.full_name")

    class Meta:
        model = Task
        fields = ['id', 'title', 'start_date_time', 'driver', 'truck']


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'


class TruckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Truck
        fields = '__all__'

