



from django.contrib.auth import get_user_model
from django.db import models

from .models import *
from .product import *

User = get_user_model()


class Wishlist(BaseModel):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    items = models.ManyToManyField(Product, related_name='wishlists', blank=True)

    def __str__(self):
        return f'{self.user.username} - {self.name if self.name else "Wishlist"}'

    class Meta:
        unique_together = ('user', 'name')
