

from django.contrib.auth import get_user_model
from django.db import models

from .models import *

User = get_user_model()


class Category(BaseModel):

    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="category_images", null=True, blank=True)
