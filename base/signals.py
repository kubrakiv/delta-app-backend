from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.db.utils import IntegrityError
from user.models import DriverProfile
from base.models import Truck, Trailer, TrailerAssignment, DriverAssignment


@receiver(pre_save, sender=Truck)
def handle_trailer_assignment(sender, instance, **kwargs):
    try:
        old_truck = Truck.objects.get(pk=instance.pk)
        previous_trailer = old_truck.trailer
    except Truck.DoesNotExist:
        previous_trailer = None

    new_trailer = instance.trailer

    # If the trailer has changed, update the assignments
    if previous_trailer != new_trailer:
        # Mark the previous TrailerAssignment as inactive
        if previous_trailer:
            previous_assignment = TrailerAssignment.objects.filter(
                truck=instance,
                trailer=previous_trailer,
                is_active=True,
            ).first()
            if previous_assignment:
                previous_assignment.end_date = timezone.now()
                previous_assignment.is_active = False
                previous_assignment.save()

@receiver(post_save, sender=Truck)
def create_trailer_assignment(sender, instance, created, **kwargs):
    if instance.trailer:
        # Create a new TrailerAssignment object for the new trailer
        TrailerAssignment.objects.create(
            truck=instance,
            trailer=instance.trailer,
            start_date=timezone.now(),
            is_active=True,
        )

@receiver(pre_save, sender=Truck)
def handle_driver_assignment(sender, instance, **kwargs):
    try:
        old_truck = Truck.objects.get(pk=instance.pk)
        previous_driver = old_truck.driver
    except Truck.DoesNotExist:
        previous_driver = None

    new_driver = instance.driver

    # If the driver has changed, update the assignments
    if previous_driver != new_driver:
        # Mark the previous DriverAssignment as inactive
        if previous_driver:
            previous_assignment = DriverAssignment.objects.filter(
                truck=instance,
                driver_profile=previous_driver,
                is_active=True,
            ).first()
            if previous_assignment:
                previous_assignment.end_date = timezone.now()
                previous_assignment.is_active = False
                previous_assignment.save()

@receiver(post_save, sender=Truck)
def create_driver_assignment(sender, instance, created, **kwargs):
    if instance.driver:
        # Create a new DriverAssignment object for the new driver
        DriverAssignment.objects.create(
            truck=instance,
            driver_profile=instance.driver,
            start_date=timezone.now(),
            is_active=True,
        )


