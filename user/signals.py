from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Profile,  DriverProfile


@receiver(pre_save, sender=Profile)
def update_user_username(sender, instance, **kwargs):
    # Ensure the username is set to the email if not already set
    if not instance.username and instance.email:
        instance.username = instance.email


@receiver(post_save, sender=Profile)
def create_or_update_driver_profile(sender, instance, created, **kwargs):
    if created or (instance.role.name == "driver" and not hasattr(instance, 'driverprofile')):
        create_driver_profile(instance)
    elif instance.role and instance.role.name == "driver":
        update_driver_profile(instance)

def create_driver_profile(profile):
    # Create the DriverProfile instance for the profile
    full_name = f"{profile.first_name} {profile.last_name}"
    DriverProfile.objects.create(
        profile=profile, 
        phone_number=profile.phone_number,
        first_name=profile.first_name,
        last_name=profile.last_name,
        full_name=full_name,
        email=profile.email,
        )


def update_driver_profile(profile):
    # Update the DriverProfile instance for the profile
    try:
        driver_profile = profile.driverprofile
    except DriverProfile.DoesNotExist:
        # If the profile does not exist, you might want to create it
        create_driver_profile(profile)
        return

    driver_profile.phone_number = profile.phone_number
    driver_profile.email = profile.email
    driver_profile.save()
