from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
import os
from .models import Profile
from django.utils import timezone


@receiver(signal=post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(signal=post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    instance.profile.save()


@receiver(signal=pre_delete, sender=User)
def log_deleted_user(sender, instance, **kwargs):
    with open("logs/deleted_user.log", "a", encoding="utf-8") as f:
        f.write(
            f"---\n{instance.username} deleted - {timezone.now()}. Food owner changed to admin.\n---\n")


@receiver(signal=pre_delete, sender=User)
def remove_user_image(sender, instance, **kwargs):
    profil = Profile.objects.filter(user=instance).first()
    if profil.image:
        os.remove(profil.image.path)
