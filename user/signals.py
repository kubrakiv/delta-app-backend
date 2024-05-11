from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import User, Role, DriverProfile


@receiver(pre_save, sender=User)
def update_user_username(sender, instance, **kwargs):
    # Ensure the username is set to the email if not already set
    if not instance.username and instance.email:
        instance.username = instance.email


@receiver(post_save, sender=User)
def create_or_update_driver_profile(sender, instance, created, **kwargs):
    if created or (instance.role.name == "driver" and not hasattr(instance, 'driverprofile')):
        create_driver_profile(instance)
    else:
        update_driver_profile(instance)

def create_driver_profile(user):
    # Create the DriverProfile instance for the user
    full_name = f"{user.first_name} {user.last_name}"
    DriverProfile.objects.create(
        user=user, 
        phone_number=user.phone_number,
        first_name=user.first_name,
        last_name=user.last_name,
        full_name=full_name,
        email=user.email,
        )


def update_driver_profile(user):
    # Update the DriverProfile instance for the user
    try:
        driver_profile = user.driverprofile
    except DriverProfile.DoesNotExist:
        return

    driver_profile.phone_number = user.phone_number
    driver_profile.email = user.email
    driver_profile.save()
