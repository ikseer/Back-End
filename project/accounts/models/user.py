
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from .model import *


class CustomUser(AbstractUser,BaseModel):
    id=models.UUIDField(default=uuid.uuid4, editable=False, unique=True ,primary_key=True)
    user_type = models.CharField(max_length=255, choices=(('patient', 'Patient'), ('doctor', 'Doctor')),default='patient')




class Profile(BaseModel):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="profile_image", blank=True, null=True)
    bio = models.TextField(blank=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=255, blank=True)
    timezone = models.CharField(max_length=255, blank=True, default="Africa/Cairo")



    class Meta:
        abstract = True
