# -*- coding: utf-8 -*-
from accounts.models import *
from django.contrib.auth import get_user_model

User = get_user_model()



# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         profile=POSITIONS[instance.user_type]
#         profile.objects.create(user=instance)
#         print(profile)




# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
# #set profile as completed when profile is updated


# @receiver(post_save, sender=Profile)
# def update_profile(sender, instance, **kwargs):
#     """
#     A signal receiver which sets the profile as completed
#     when the UserProfile model is updated.
#     """

#     if not instance.is_completed:
#         instance.is_completed = True
#         instance.save()
