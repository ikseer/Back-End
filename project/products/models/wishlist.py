



from django.contrib.auth import get_user_model
from django.db import models

from .models import *
from .product import *

User = get_user_model()


class Wishlist(BaseModel):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.user.username} - "Wishlist"'

class WishlistItem(BaseModel):

    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)

    class Meta:
            unique_together = ('wishlist', 'product')

    def __str__(self):
        return f"{self.product.name} in cart of {self.wishlist.user.username}"
