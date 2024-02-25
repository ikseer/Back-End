from paymob.accept import AcceptAPIClient

from .models import PaymobOrder

accept_api_client = AcceptAPIClient()
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

    code, response_order, feedback = accept_api_client.get_order(
        order_id=paymob_order_id
    )
    order_paying=PaymobOrder.objects.get(paymob_order_id=paymob_order_id)
    return order_paying.amount_cents>=response_order.amount_cents
