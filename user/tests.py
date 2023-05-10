from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from collections import defaultdict
from user.models import User


# Create your tests here.


class UserSignOutTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create_user(
            username="zxcvbnasdf_",
            email="abcd@naver.com",
            password="asdf1234!!",
        )
        cls.user_data = {"username": "zxcvbnasdf_", "password": "asdf1234!!"}

    def setUp(self) -> None:
        self.access = self.client.post(reverse("token"), self.user_data).data["access"]

    def test_logined(self):
        url = reverse("signup/out")
        response = self.client.put(
            path=url,
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
            data=self.user_data,
        )
        self.assertEqual(response.status_code, 200)

    def test_annon(self):
        url = reverse("signup/out")
        response = self.client.put(
            path=url,
            data=self.user_data,
        )
        self.assertEqual(response.status_code, 401)

    def test_wrong_password(self):
        url = reverse("signup/out")
        response = self.client.put(
            path=url,
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
            data={"password": "asdf!!1234"},
        )
        self.assertEqual(response.status_code, 400)

    def test_wrong_token(self):
        url = reverse("signup/out")
        response = self.client.put(
            path=url,
            HTTP_AUTHORIZATION=f"Bearer {self.access[:-3]}123",
            data=self.user_data,
        )
        self.assertEqual(response.status_code, 401)
