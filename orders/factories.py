# myapp/factories.py

import factory
from faker import Faker
from orders.models import Order

fake = Faker()

class OrderFactory(factory.Factory):
    class Meta:
        model = Order

    # patient = factory.SubFactory('accounts.factories.ProfileFactory')
    # customer = factory.SubFactory('accounts.factories.ProfileFactory')
    # customer=factory.SubFactory('accounts.factories.ProfileFactory')
    
    # total_price = factory.Faker('random_int', min=1, max=1000)
    pharmacy = factory.SubFactory('pharmacy.factories.PharmacyFactory')
    status='Pending'
