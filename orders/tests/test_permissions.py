from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from orders.models import *
from pharmacy.models import *
from products.models import *

User = get_user_model()
from rest_framework.test import APIClient


class PermissionTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="usual_user", email="usual@example.com", password="test_password"
        )
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
            {"customer": self.user.id, "pharmacy": self.pharmacy.id},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_user_create_order_permission(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")

        response = self.client.post(
            "/orders/orders/",
            {"customer": self.user.id, "pharmacy": self.pharmacy.id},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_auth_user_update_order_permission(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        order = self.client.post(
            "/orders/orders/",
            {"customer": self.user.id, "pharmacy": self.pharmacy.id},
            format="json",
        ).data
        response = self.client.put(
            "/orders/orders/" + str(order["id"]) + "/",
            {
                "customer": self.user.id,
                "pharmacy": self.pharmacy.id,
                "status": "Delivered",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_user_update_order_permission(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        order = self.client.post(
            "/orders/orders/",
            {"customer": self.user.id, "pharmacy": self.pharmacy.id},
            format="json",
        ).data
        response = self.client.put(
            "/orders/orders/" + str(order["id"]) + "/",
            {"customer": self.user.id, "pharmacy": self.pharmacy.id},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_auth_user_delete_order_permission(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        order = self.client.post(
            "/orders/orders/",
            {"customer": self.user.id, "pharmacy": self.pharmacy.id},
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
            {"customer": self.user.id, "pharmacy": self.pharmacy.id},
            format="json",
        ).data
        response = self.client.delete(
            "/orders/orders/" + str(order["id"]) + "/", format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_order_of_another_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        own_order = self.client.post(
            "/orders/orders/",
            {"customer": self.user.id, "pharmacy": self.pharmacy.id},
            format="json",
        ).data
        user2 = User.objects.create_user(
            username="user2", email="user2@example.com", password="test_password"
        )
        order_another_user = self.client.post(
            "/orders/orders/",
            {"customer": user2.id, "pharmacy": self.pharmacy.id},
            format="json",
        ).data
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
