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
    user_type = models.CharField(max_length=10, choices=(('patient', 'Patient'), ('doctor', 'Doctor')),default='patient')




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
    timezone = models.CharField(max_length=50, blank=True, default="Africa/Cairo")



    class Meta:
        abstract = True


class Patient(Profile):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.first_name + " " + self.last_name)

    def is_patient():
        return True

class Doctor(Profile):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    location = models.CharField(max_length=255,null=True,blank=True)
    price_for_reservation=models.IntegerField(null=True,blank=True)
    approved = models.BooleanField(default=False)


    def __str__(self):
        return str(self.first_name + " " + self.last_name)

    def is_doctor():
        return True



POSITIONS={
     'patient':Patient,
     'doctor':Doctor
}
