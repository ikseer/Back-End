

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from safedelete.managers import SafeDeleteManager

from .model import *


class CustomUserManager(SafeDeleteManager, UserManager):
    pass


class CustomUser(BaseModel,AbstractUser):

    _safedelete_policy =SOFT_DELETE_CASCADE
    objects = CustomUserManager()
    user_type = models.CharField(max_length=255, choices=(('patient', 'Patient'), ('doctor', 'Doctor'),('employee','Employee')),default='patient')




class Profile(BaseModel):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="profile_image", blank=True, null=True)
    bio = models.TextField(blank=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    date_of_birth = models.CharField(max_length=255,blank=True, null=True)
    gender = models.CharField(max_length=255, blank=True)
    timezone = models.CharField(max_length=255, blank=True, default="Africa/Cairo")



    class Meta:
        abstract = True
