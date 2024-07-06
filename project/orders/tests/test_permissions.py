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


class PermissionTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="usual_user", email="usual@example.com", password="test_password"
        )
        EmailAddress.objects.create(user=self.user,email=self.user.email,verified=True)

        self.admin_user = User.objects.create_user(
            username="admin_user",
            email="admin@example.com",
            password="test_password",
            is_staff=True,
        )
        self.client = APIClient()
        self.user_token = self.get_token(self.user)
        self.admin_token = self.get_token(self.admin_user)
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
            # pharmacy=self.pharmacy,
                        stock=10

        )
        self.cart=Cart.objects.get(user=self.user)
        CartItem.objects.create(cart=self.cart,product=self.product1,quantity=3)
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
    def get_token(self, user):
        url = reverse("rest_login")
        response = self.client.post(
            url, {"email": user.email, "password": "test_password"}
        )
        return response.data["access"]

    def test_usual_user_order_permission(self):
        response = self.client.get("/orders/orders/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_auth_user_create_order_permission(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")

        response = self.client.post(
            "/orders/orders/",
             self.order_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_user_create_order_permission(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")

        response = self.client.post(
            "/orders/orders/",
             self.order_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_auth_user_update_order_permission(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        order = self.client.post(
            "/orders/orders/",
             self.order_data,
            format="json",
        ).data
        response = self.client.put(
            "/orders/orders/" + str(order["id"]) + "/",
             self.order_data,
            format="json",
        )
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_user_update_order_permission(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        order = self.client.post(
            "/orders/orders/",
         self.order_data,
            format="json",
        ).data
        response = self.client.put(
            "/orders/orders/" + str(order["id"]) + "/",
             self.order_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_auth_user_delete_order_permission(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        order = self.client.post(
            "/orders/orders/",
             self.order_data,
            format="json",
        ).data
        response = self.client.delete(
            "/orders/orders/" + str(order["id"]) + "/", format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_admin_user_delete_order_permission(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        order = self.client.post(
            "/orders/orders/",
             self.order_data,
            format="json",
        ).data
        response = self.client.delete(
            "/orders/orders/" + str(order["id"]) + "/", format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_order_of_another_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        self.client.post(
            "/orders/orders/",
             self.order_data,
            format="json",
        ).data
        user2 = User.objects.create_user(
            username="user2", email="user2@example.com", password="test_password"
        )
        EmailAddress.objects.create(user=user2,email=user2.email,verified=True)

        cart=Cart.objects.get(user=user2)
        CartItem.objects.create(cart=cart,product=self.product1,quantity=2)
        # usr2=User.objects.get(  username="user2")
        self.order_data['user']=user2.id
        order_another_user = self.client.post(
            "/orders/orders/",
            self.order_data,
            format="json",
        ).data
        # print(order_another_user)
        response = self.client.delete(
            "/orders/orders/" + str(order_another_user["id"]) + "/", format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        user2_token = self.get_token(user2)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {user2_token}")
        response = self.client.delete(
            "/orders/orders/" + str(order_another_user["id"]) + "/", format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
