from django.db.models.signals import pre_save
from .models import BlogPost
from django.dispatch import receiver
import os


@receiver(pre_save, sender=BlogPost)
def delete_old_file(sender, instance, **kwargs):
    # on creation, signal callback won't be triggered
    if instance._state.adding and not instance.pk:
        return False
    try:
        old_file = sender.objects.get(pk=instance.pk).image
    except sender.DoesNotExist:
        return False

    # comparing the new file with the old one
    file = instance.image
    if not old_file == file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
