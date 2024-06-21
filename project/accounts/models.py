# -*- coding: utf-8 -*-
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class BaseModel(models.Model):

    id=models.UUIDField(default=uuid.uuid4, editable=False, unique=True ,primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class CustomUser(AbstractUser):
    id=models.UUIDField(default=uuid.uuid4, editable=False, unique=True ,primary_key=True)




class EmailVerificationOTP(BaseModel):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    otp = models.IntegerField(null=True, blank=True)
    activation_key = models.CharField(max_length=150, blank=True, null=True)


class PhoneModel(BaseModel):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    Mobile = models.CharField(max_length=20, blank=False)
    isVerified = models.BooleanField(blank=False, default=False)
    counter = models.IntegerField(default=0, blank=False)

    def __str__(self):
        return str(self.Mobile)


class Profile(BaseModel):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="profile_image", blank=True, null=True)
    bio = models.TextField(blank=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=255, blank=True)
    is_completed = models.BooleanField(default=False)
    timezone = models.CharField(max_length=50, blank=True, default="Africa/Cairo")

    def __str__(self):
        return str(self.first_name + " " + self.last_name)


class PatientProfile(BaseModel):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)


class DoctorProfile(BaseModel):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
