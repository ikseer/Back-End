
from .models import *


class Cart(models.Model):
    id=models.UUIDField(default=uuid.uuid4, editable=False ,primary_key=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart',null=True ,unique=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    # products = models.ManyToManyField('products.Product', through='CartItem',related_name='items')
    def get_items(self):
        return self.cartitem_set.select_related('product')

    def __str__(self):
        return f"Cart of {self.user.username}"

    def get_total_price(self):
        total = sum(item.get_total_price() for item in self.items.all())
        return total

class CartItem(models.Model):
    id=models.UUIDField(default=uuid.uuid4, editable=False, unique=True ,primary_key=True)

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in cart of {self.cart.user.username}"

    def get_total_price(self):
        return self.product.get_final_price() * self.quantity
