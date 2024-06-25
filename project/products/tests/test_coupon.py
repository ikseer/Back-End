# -*- coding: utf-8 -*-

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
            pharmacy=self.pharmacy,
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
            "discount_amount": 30,
            "start_date": "2022-01-01",
            "end_date": "2022-12-31",

        }
        response = self.client.post(
            url,
            data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    def test_create_coupon(self):
        url = "/products/coupon/"
        data = {
            "product": self.product.id,
            "discount_amount": 30,
            "start_date": "2022-01-01",
            "end_date": "2022-12-31",
            "code": "test_co",

        }
        response = self.client.post(
            url,
            data,
            format="json",
            HTTP_AUTHORIZATION="Bearer " + self.admin_token,
        )
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    def test_edit_coupon(self):
        url = f"/products/coupon/{self.coupon1.id}/"
        data = {

            "discount_amount": 30,
            "start_date": "2022-01-01",
            "end_date": "2022-12-31",

        }
        response = self.client.put(
            url,
            data,
            format="json",
            HTTP_AUTHORIZATION="Bearer " + self.admin_token,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_delete_coupon(self):
        url = f"/products/coupon/{self.coupon1.id}/"
        response = self.client.delete(
            url,
            format="json",
            HTTP_AUTHORIZATION="Bearer " + self.admin_token,
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    def test_get_coupon(self):
        url = f"/products/coupon/{self.coupon1.id}/"
        response = self.client.get(
            url,
            format="json",
            HTTP_AUTHORIZATION="Bearer " + self.admin_token,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_get_all_coupons(self):
        url = "/products/coupon/"
        response = self.client.get(
            url,
            format="json",
            HTTP_AUTHORIZATION="Bearer " + self.admin_token,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_deactivate_coupon(self):
        url = f"/products/coupon/{self.coupon1.id}/"
        data={
            "active":False
        }
        response = self.client.patch(
            url,
            data,
            format="json",
            HTTP_AUTHORIZATION="Bearer " + self.admin_token,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
