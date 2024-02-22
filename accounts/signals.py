from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()

from accounts.models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        # pro=Profile.objects.get(user=instance)
        # print('profile created',pro.id)


# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
# #set profile as completed when profile is updated


@receiver(post_save, sender=Profile)
def update_profile(sender, instance, **kwargs):
    """
    A signal receiver which sets the profile as completed when the UserProfile model is updated.
    """

    if not instance.is_completed:
        instance.is_completed = True
        instance.save()
