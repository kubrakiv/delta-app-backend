from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Role(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class Profile(AbstractUser):
    role = models.ForeignKey(Role, related_name="profiles", on_delete=models.CASCADE, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.username

  
class AdminProfile(models.Model):
    profile = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, primary_key = True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    position = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.profile.username + " " + self.position


class LogistProfile(models.Model):
    profile = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, primary_key = True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    position = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.profile.username + " " + self.position

class DriverProfile(models.Model):
    profile = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, primary_key = True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    middle_name = models.CharField(max_length=255, null=True, blank=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    position = models.CharField(max_length=255, null=True, blank=True)
    license_series = models.CharField(max_length=255, blank=True, null=True)
    license_number = models.CharField(max_length=255, blank=True, null=True)
    birth_date = models.DateField(auto_now_add=False, null=True, blank=True)
    started_work = models.DateField(auto_now_add=False, null=True, blank=True)
    finished_work = models.DateField(auto_now_add=False, null=True, blank=True)
    country = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        if self.full_name:
            return self.full_name
        else:
            return self.profile.username


