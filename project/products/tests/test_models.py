# -*- coding: utf-8 -*-
# class ProductViewSetTests(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.product1 = Product.objects.create(name='Product1', price=50, category='Electronics')
#         self.product2 = Product.objects.create(name='Product2', price=30, category='Clothing')
#     def test_get_all_products(self):
#         response = self.client.get('/products/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 2)
#     def test_filter_by_name(self):
#         response = self.client.get('/products/', {'name': 'Product1'})
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)
#         self.assertEqual(response.data[0]['name'], 'Product1')
#     def test_filter_by_price(self):
#         response = self.client.get('/products/', {'price': 30})
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)
#         self.assertEqual(response.data[0]['price'], '30.00')
# Add more tests for other filters as needed

from django.test import TestCase
from django.urls import reverse
from orders.models import *
from pharmacy.models import *
from products.models import *
from rest_framework import status
from rest_framework.test import APIClient


class CouponViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin=User.objects.create_superuser(
            username="test_admin", email="test2@example.com", password="test_password" )
        response=self.client.post(
            reverse("rest_login"),
            {"email": self.admin.email, "password": "test_password"},
        )
        self.admin_token = response.data["access"]
        self.category=Category.objects.create(name="test_category")
        self.pharmacy=Pharmacy.objects.create(name="test_pharmacy")
        self.product=Product.objects.create(
            name="test_product",
            generic_name="test_generic_name",
            form="test_form",
            strength="test_strength",
            factory_company="test_factory_company",
            short_description="test_short_description",
            description="test_description",
            price=100,
            category=self.category,
            # pharmacy=self.pharmacy,
            stock=10,
            code="test_code",
        )
        self.coupon1=Coupon.objects.create(
            code="test_coupon1",
            discount_amount=30,
            start_date="2022-01-01",
            end_date="2022-12-31",
        )



    def test_create_coupon_not_admin(self):
        url = "/products/coupon/"
        data = {
            "product": self.product.id,
            "percentage": 30,
            "start_date": "2022-01-01",
            "end_date": "2022-12-31",

        }
        response = self.client.post(
            url,
            data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
