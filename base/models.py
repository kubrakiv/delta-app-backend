from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Truck(models.Model):
    plates = models.CharField(max_length=25)

    def __str__(self):
        return self.plates
    

class Driver(models.Model):
    full_name = models.CharField(max_length=255)

    def __str__(self):
        return self.full_name
    

class Task(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    start_date_time = models.DateTimeField(auto_now_add=False, null=False, blank=False)
    truck = models.ForeignKey(Truck, on_delete=models.SET_NULL, null=True, blank=True)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.title
    