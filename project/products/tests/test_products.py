# -*- coding: utf-8 -*-
from django.test import TestCase
from django.urls import reverse
from orders.models import *
from pharmacy.models import Pharmacy
from products.models import *
from rest_framework import status
from rest_framework.test import APIClient

# from rest_framework import status


class ProductViewSetTests(TestCase):
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
        # order = Order.objects.create(pharmacy=self.pharmacy)
        # self.order_item = OrderItem.objects.create(
        #     product=self.product3, quantity=2, order=order
        # )
        self.url = "/products/product/"
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
        self.user = User.objects.create_user(
            username="test_user", email="test1@example.com", password="test_password"
        )
        # get token
        self.user_token = self.get_token(self.user)

        self.admin = User.objects.create_superuser(
            username="test_admin", email="test2@example.com", password="test_password"
        )
        self.admin_token = self.get_token(self.admin)

    def get_token(self, user):
        url = reverse("rest_login")
        response = self.client.post(
            url, {"email": user.email, "password": "test_password"}
        )
        return response.data["access"]

    def test_list_products(self):
        response = self.client.get(self.url)
        # data = response.data["results"]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(len(data), 3)

    def test_retrieve_product(self):
        response = self.client.get(self.url + str(self.product.id) + "/")
        data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["name"], "Test Product1")
        print(response.data)
    def test_create_product_not_staff(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")

        response = self.client.post(self.url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_product(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")

        response = self.client.post(self.url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_product_not_staff(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")

        response = self.client.put(
            self.url + str(self.product.id) + "/", self.data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_product(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")

        response = self.client.put(
            self.url + str(self.product.id) + "/", self.data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_product_not_staff(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")

        response = self.client.delete(
            self.url + str(self.product.id) + "/", format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_product(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")

        response = self.client.delete(
            self.url + str(self.product.id) + "/", format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


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
        self.url = "/products/product/"
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
        response = self.client.get(self.url, {"name__icontains": "Test Product1"})
        # print(response.data['results'])
        data = response.data["results"]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], "Test Product1")

    def test_filter_by_price(self):
        response = self.client.get(self.url, {"price__gte": 20, "price__lte": 30})
        data = response.data["results"]
        # data=response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        prices = [item["price"] for item in data]
        self.assertEqual(max(prices) <= 30, True)
        self.assertEqual(min(prices) >= 20, True)

    def test_filter_by_top_sales(self):
        response = self.client.get(self.url, {"top_sales": "True"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_by_category(self):
        response = self.client.get(self.url, {"category": self.category.id})
        data = response.data["results"]
        # data=response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 3)

    def test_pagination(self):
        # create 25 products
        for i in range(25):
            Product.objects.create(
                name=f"Test Product {i}",
                price=20.0,
                strength=5,
                category=self.category,
                pharmacy=self.pharmacy,
            )
        url = "/products/product/"
        response = self.client.get(url + "?page=1&limit=15")
        data = response.data["results"]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 15)
        response = self.client.get(url + "?page=2&limit=8")
        data = response.data["results"]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 8)
        response = self.client.get(url)
        data = response.data["results"]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # print(data,len(Product.objects.all()))
        # self.assertEqual(len(data), 20)
