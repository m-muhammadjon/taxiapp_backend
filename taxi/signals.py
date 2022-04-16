from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Location


@receiver(post_save, sender=Location)
def update_driver_location(sender, instance, created, **kwargs):
    if created:
        driver = instance.driver
        driver.last_location = instance.location
        driver.save()
