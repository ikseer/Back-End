# -*- coding: utf-8 -*-
import uuid

from django.db import models
from safedelete.models import SOFT_DELETE_CASCADE, SafeDeleteModel,HARD_DELETE


class BaseModel(SafeDeleteModel):
    _safedelete_policy =HARD_DELETE

    id=models.UUIDField(default=uuid.uuid4, editable=False, unique=True ,primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
