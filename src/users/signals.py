from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=User)
# post_save is the signal which is received by the receiver
# receiver is the function that gets this signal and performs some task
def create_profile(sender, instance, created, **kwargs): # to create the profile
	if created:
		Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs): # to save the profile
	instance.profile.save()

