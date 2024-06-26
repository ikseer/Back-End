# -*- coding: utf-8 -*-
import uuid

from django.db import models


class BaseModel(models.Model):

    id=models.UUIDField(default=uuid.uuid4, editable=False, unique=True ,primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Pharmacy(BaseModel):

    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to="pharmacy_images/", null=True, blank=True)
    open_time = models.TimeField(default="00:00:00")
    close_time = models.TimeField(default="00:00:00")
    phone = models.CharField(max_length=20)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    def __str__(self):
        return self.name
