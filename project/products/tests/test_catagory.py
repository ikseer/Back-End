# -*- coding: utf-8 -*-
from allauth.account.models import EmailAddress
from django.test import TestCase
from django.urls import reverse
from orders.models import *
from products.models import *
from rest_framework import status
from rest_framework.test import APIClient

# from rest_framework import status

# from rest_framework import status


class CategoryViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category1 = Category.objects.create(
            name="Electronics", image="electronics.jpg"
        )
        self.category2 = Category.objects.create(name="Clothing")
        self.url = "/products/category/"
        self.user = User.objects.create_user(
            username="test_user", email="test1@example.com", password="test_password"
        )
        EmailAddress.objects.create(user=self.user,verified=True)

        # get token
        self.user_token = self.get_token(self.user)
        self.admin = User.objects.create_superuser(
            username="test_admin", email="test2@example.com", password="test_password"
        )
        # EmailAddress.objects.create(user=self.admin,verified=True)

        self.admin_token = self.get_token(self.admin)
        # print(self.admin_token )

    def get_token(self, user):
        url = reverse("rest_login")
        response = self.client.post(
            url, {"email": user.email, "password": "test_password"}
        )
        return response.data["access"]

    def test_get_all_categories(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_by_name(self):
        response = self.client.get(
            "/products/category/", {"name__icontains": "Electronics"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Electronics")

        response = self.client.get(
            "/products/category/", {"name__icontains": "Electronics"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Electronics")

    def test_create_category_not_auth(self):
        data = {"name": "Furniture"}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_category_not_staff(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        data = {"name": "Furniture"}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_category(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        data = {"name": "Furniture"}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_category(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        data = {"name": "Furniture"}
        response = self.client.put(
            f"/products/category/{ self.category1.id}/", data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_category(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        response = self.client.delete(f"/products/category/{ self.category1.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_category(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        id = Category.objects.get(name="Electronics").id
        response = self.client.get(f"/products/category/{id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_nonexistent_category(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        response = self.client.get("/products/category/1000/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
