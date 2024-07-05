# -*- coding: utf-8 -*-
from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from orders.models import *
from pharmacy.models import *
from products.models import *
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()


class OrderItemTest(TestCase):
    def setUp(self) -> None:
        user = User.objects.create_user(
            username="test_user", email="test@example.com", password="test_password"
        )
        self.client = APIClient()
        url = reverse("rest_login")
        EmailAddress.objects.create(user=user,email=user.email,verified=True)
        response = self.client.post(
            url, {"email": "test@example.com", "password": "test_password"}
        )

        self.access_token = response.data["access"]
        self.category = Category.objects.create(name="Test category")
        self.pharmacy = Pharmacy.objects.create(
            name="Test pharmacy",
            location="Test location",
            image="test_data/images/pharmacy/image.jpg",
            open_time="09:00:00",
            close_time="18:00:00",
            phone="1234567890",
        )
        self.product1 = Product.objects.create(
            category=self.category,
            name="Product 1",
            description="Test description",
            price=50.00,
            pharmacy=self.pharmacy,
            stock=10
        )
        self.product2 = Product.objects.create(
            category=self.category,
            name="Product 2",
            description="Test description",
            price=100.00,
            pharmacy=self.pharmacy,
            stock=10

        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        cart=Cart.objects.get(user=user)
        CartItem.objects.create(cart=cart,product=self.product1,quantity=3)
        self.order_data = {
            "user": self.user.id,
             'first_name': 'John',
            'last_name': 'Doe',
            'country': 'USA',
            'city': 'New York',
            'street': '123 Main St',
            'zip_code': '10001',
            'phone': '123-456-7890',
            'email': 'john.doe@example.com',
            # "pharmacy": self.pharmacy.id,
        }
        self.order = self.client.post(
            "/orders/orders/",
            self.order_data,
            format="json",
        ).data

        self.order_item_data = {
            "product": self.product1.id,
            "quantity": 2,
            "order": self.order["id"],
        }

    # def create_order_item(self):
    #     response = self.client.post(
    #         "/orders/orderItem/", self.order_item_data, format="json"
    #     )
    #     return response.data

    def test_get_order_items(self):
        # self.create_order_item()
        response = self.client.get("/orders/order-item/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
