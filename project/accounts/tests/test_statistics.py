# -*- coding: utf-8 -*-

from accounts.models import *
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase

User=get_user_model()
# testcase

# testcase


class DoctorTest(APITestCase):
    def setUp(self):
        pass



    def test_get_statistics(self):
        url = reverse("dashboard")
        response=self.client.get(url)
        self.assertEqual(response.status_code,200)
        self.assertIn("total_products",response.data)
