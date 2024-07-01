



from django.contrib.auth import get_user_model
from django.db import models

from .models import *

User = get_user_model()


class ProductImage(BaseModel):

    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="product_images", null=True, blank=True)
    priority = models.IntegerField(default=1, null=True, blank=True)

    def __str__(self):
        return self.product.name
