# -*- coding: utf-8 -*-
import uuid

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()



class BaseModel(models.Model):

    id=models.UUIDField(default=uuid.uuid4, editable=False, unique=True ,primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
