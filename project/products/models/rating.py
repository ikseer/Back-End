


from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .models import *
from .product import *

User = get_user_model()
class ProductRating(BaseModel):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True
    )
    review = models.TextField(blank=True, null=True)


    class Meta:
        unique_together = ('user', 'product')


    def __str__(self):
        return f'{self.user.username} - {self.product.name} - {self.rating}'
