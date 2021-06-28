from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


@receiver(post_save, sender=User)
def build_profile(sender, instance, created, **kwags):
    """
        sender will be the signal responsible
        instance is the User which has been saved
        created is a boolean which shows if the user has been created or not
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwags):
    instance.profile.save()

