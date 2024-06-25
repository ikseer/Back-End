# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from orders.models import *
from pharmacy.models import *
from products.models import *
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()


class OrderTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user", email="test@example.com", password="test_password"
        )
        self.pharmacy = Pharmacy.objects.create(
            name="Test pharmacy",
            location="Test location",
            image="test_data/images/pharmacy/image.jpg",
            open_time="09:00:00",
            close_time="18:00:00",
            phone="1234567890",
        )
        self.category = Category.objects.create(name="Test category")
        self.product1 = Product.objects.create(
            category=self.category,
            name="Product 1",
            description="Test description",
            price=50.00,
            pharmacy=self.pharmacy,
        )
        self.product2 = Product.objects.create(
            category=self.category,
            name="Product 2",
            description="Test description",
            price=100.00,
            pharmacy=self.pharmacy,
        )

        self.client = APIClient()
        url = reverse("rest_login")
        response = self.client.post(
            url, {"email": "test@example.com", "password": "test_password"}
        )
        self.access_token = response.data["access"]
        self.order_data = {
            "user": self.user.id,
            "pharmacy": self.pharmacy.id,
        }
        cart = self.client.get("/orders/cart/",HTTP_AUTHORIZATION=f"Bearer {self.access_token}").data
        self.data={
            'product':self.product1.id,
            'quantity':3,
            'cart':cart['id']

        }
        self.client.post("/orders/cart-item/",data=self.data,format='json',HTTP_AUTHORIZATION=f"Bearer {self.access_token}").data


    def create_order(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        response = self.client.post("/orders/orders/", self.order_data, format="json")
        return response.data

    def test_create_order(self):
        response = self.client.post("/orders/orders/", self.order_data, format="json",HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(OrderItem.objects.count(),1)
        self.assertEqual(CartItem.objects.count(),0)

    def test_update_order(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        order = self.create_order()
        response = self.client.put(
            "/orders/orders/" + str(order["id"]) + "/", self.order_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_order(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        order = self.create_order()
        response = self.client.delete(
            "/orders/orders/" + str(order["id"]) + "/", self.order_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_orders(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        self.create_order()
        response = self.client.get("/orders/orders/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
