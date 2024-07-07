# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from pharmacy.models import Pharmacy
from products.models import Category, Product
from rest_framework.test import APIClient

User=get_user_model()

class PharmacyViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.category = Category.objects.create(name="Test Category")
        self.pharmacy = Pharmacy.objects.create(
            name="Test Pharmacy", phone="1234567890"
        )
        self.product = Product.objects.create(
            name="Test Product",
            price=10.0,
            strength=5,
            category=self.category,
            # pharmacy=self.pharmacy,
        )

        self.url = reverse("pharmacy-list")
        self.admin = User.objects.create_superuser(
            username="test_admin", email="test2@example.com", password="test_password"
        )
        # EmailAddress.objects.create(user=self.admin,verified=True)

        self.admin_token = self.get_token(self.admin)
    def get_token(self, user):
            url = reverse("rest_login")
            response = self.client.post(
                url, {"email": user.email, "password": "test_password"}
            )
            return response.data["access"]
    def test_get_pharmacy(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]["name"], "Test Pharmacy")

    def test_create_pharmacy(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")

        data = {
            "name": "Test Pharmacy",
            "phone": "1234567890",
            "location": "Test Location",
        }
        response = self.client.post(self.url, data)
        # print(response.data)
        self.assertEqual(response.status_code, 201)

    def test_update_pharmacy(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")

        data = {
            "name": "Updated Test Pharmacy",
            # "phone": "1234567890",
            "location": "Updated Test Location"
        }
        response = self.client.patch(
            f"/pharmacy/pharmacy/{self.pharmacy.id}/",
            data,
            format="json"
        )
        # print(data,response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "Updated Test Pharmacy")
