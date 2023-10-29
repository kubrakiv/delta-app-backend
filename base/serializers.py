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
    
    def update(self, instance, validated_data):
        driver_data = validated_data.pop('driver', None)
        truck_data = validated_data.pop('truck', None)

        instance.title = validated_data.get('title', instance.title)
        instance.start_date_time = validated_data.get('start_date_time', instance.start_date_time)

        if driver_data:
            driver_instance, _ = Driver.objects.get_or_create(full_name=driver_data['full_name'])
            instance.driver = driver_instance

        if truck_data:
            truck_instance, _ = Truck.objects.get_or_create(plates=truck_data['plates'])
            instance.truck = truck_instance

        instance.save()
        return instance


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'


class TruckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Truck
        fields = '__all__'

