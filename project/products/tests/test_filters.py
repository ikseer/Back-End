# -*- coding: utf-8 -*-
from django.test import TestCase
from orders.models import *
from pharmacy.models import Pharmacy
from products.models import *
from rest_framework import status
from rest_framework.test import APIClient

# from rest_framework import status

class FilterProductViewSetTests(TestCase):
    def setUp(self):
        # Create some test data
        self.pharmacy = Pharmacy.objects.create(name="Test Pharmacy")
        self.category = Category.objects.create(name="Test Category1")
        self.product = Product.objects.create(
            name="Test Product1",
            price=20.0,
            strength=5,
            category=self.category,
            pharmacy=self.pharmacy,
        )
        self.product2 = Product.objects.create(
            name="Test Product2",
            price=30.0,
            strength=5,
            category=self.category,
            pharmacy=self.pharmacy,
        )
        self.product3 = Product.objects.create(
            name="Test Product3",
            price=25.0,
            strength=5,
            category=self.category,
            pharmacy=self.pharmacy,
        )
        self.url = "/products/home/"
        self.data = {
            "name": "Test Product",
            "price": 30.0,
            "strength": 8,
            "category": self.category.id,
            "generic_name": "Generic Name",
            "form": "Form",
            "factory_company": "Factory Company",
            "description": "Description",
            "pharmacy": self.pharmacy.id,
        }
        self.client = APIClient()

    def test_filter_by_name(self):
        Discount.objects.create(product=self.product3,discount_type='amount')
        response = self.client.get(self.url)
        data = response.data["results"]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 3)

        # response = self.client.get(self.url, {'have_discount': 'true'})
        response = self.client.get("/products/home/?have_discount=true")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # print(response.data)
        self.assertEqual(len(     response.data["results"]), 1)

        # self.assertEqual(data[0]["name"], "Test Product3")
