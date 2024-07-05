



from django.contrib.auth import get_user_model
from django.db import models

from .models import *
from .product import *

User = get_user_model()




class WishlistItem(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True,blank=True)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)

    class Meta:
            unique_together = ('user', 'product')
    def __str__(self):
        return f"{self.product.name} in cart of {self.user.username}"
