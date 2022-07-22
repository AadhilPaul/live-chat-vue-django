from django.test import TestCase
import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


# Create your tests here.

class RegistrationTestCase(APITestCase):
    def test_registration(self):
        data = {"email": "test@gmail.com", "username": "testcase",
                "password": "tvandsofa123", "re_password": "tvandsofa123"}
        response = self.client.post("/users/users/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class GetLoginTokenTestCase(APITestCase):
    def test_create_token(self):
        data = {
            "password": "tvandsofa123",
            "username": "testcase"
        }
        response = self.client.post("/users/token/login/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
