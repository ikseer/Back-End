from .models import *


class PaymobOrder(BaseModel):
    order=models.OneToOneField("orders.Order",on_delete=models.CASCADE,unique=True)
    paymob_order_id=models.CharField(max_length=255)
    paid=models.BooleanField(default=False)
    amount_cents=models.FloatField(default=0)
    currency=models.CharField(max_length=255,default="EGP")

    def __str__(self):
        return self.order.customer.username
