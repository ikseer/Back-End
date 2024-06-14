# -*- coding: utf-8 -*-
from paymob.accept import AcceptAPIClient
from paymob.accept.utils import AcceptUtils

from .models import Order, OrderItem, PaymobOrder

'''
order_id = "<Paymob Order Id>"
code, order, feedback = accept_api_client.get_order(
    order_id=order_id,
)
'''
def check_paymob_order_status(paymob_order_id : str) -> bool:
    """
    get order from paymob and check if order is paid
    Args:
        paymob_order_id (str): Paymob Order Id
    Returns:
        bool: True if order is paid else False
    """
    # integration_id = "<Your Integration ID>"
    #https://github.com/muhammedattif/Paymob-Solutions/blob/master/docs/services/accept.md#33-get-order
    try:
        PaymobOrder.objects.get(paymob_order_id=paymob_order_id)
    except PaymobOrder.DoesNotExist:
        return False
    # print(config('ACCEPT_API_KEY'))
    accept_api_client = AcceptAPIClient()
    code, response_order, feedback = accept_api_client.get_order(
        order_id=paymob_order_id
    )
    order_paying=PaymobOrder.objects.get(paymob_order_id=paymob_order_id)
    return order_paying.amount_cents>=response_order.amount_cents

def create_paymob(order_id):
    """
    create order in paymob
    Args:
        order_id (str): Order Id
    Returns:
        PaymobOrder: Paymob Order
    """
    accept_api_client = AcceptAPIClient()
    mid_key = "Type" # MidKey is useful if you support multiple types of items.
    identifier = order_id
    merchant_order_id = AcceptUtils.generate_merchant_order_id(mid_key=mid_key, identifier=identifier)
    amount_cents = calculate_amount_cents(order_id)
    currency = "EGP"

    response = accept_api_client.create_order(
        merchant_order_id=merchant_order_id,
        amount_cents=amount_cents,
        currency=currency
    )
    code , pay_order, feedback = response

    if code==10:
        paymob = PaymobOrder.objects.create(
            order_id=order_id,
            paymob_order_id=pay_order.id,
            amount_cents=amount_cents
        )
        return paymob
    else:
        return None

def calculate_product_price(product):
    return product.price
    # discount = Discount.objects.filter(product=item).first()
    # if discount is None:
    #     return item.price
    # else:
    #     percentage = discount.discount_percentage
    #     return item.price -  item.price * (percentage/100)

def calculate_amount_cents(order_id):
    order = Order.objects.get(id=order_id)
    order_items=OrderItem.objects.filter(order=order)
    amount_cents=0
    for item in order_items:
        amount_cents+=calculate_product_price(item.product)
    return amount_cents
