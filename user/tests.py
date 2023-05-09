from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from collections import defaultdict
from user.models import User


# Create your tests here.
class UserSignUpTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.data_username = defaultdict(
            lambda: [
                {
                    "email": "abcd@naver.com",
                    "password": "asdf1234!!",
                    "password2": "asdf1234!!",
                },
                400,
            ]
        )
        cls.data_username[0]
        cls.data_username[1][0]["username"] = ""
        cls.data_username[2][0]["username"] = "_abc123"
        cls.data_username[3][0]["username"] = "3a!asdf@"
        cls.data_username[4][0]["username"] = "123"

        cls.data_email = defaultdict(
            lambda: [
                {
                    "username": "zxKing_@",
                    "password": "asdf1234!!",
                    "password2": "asdf1234!!",
                },
                400,
            ]
        )
        cls.data_email[0]
        cls.data_email[5][0]["email"] = ""
        cls.data_email[1][0]["email"] = "123@123@naver.com"
        cls.data_email[2][0]["email"] = "123navercom"
        cls.data_email[3][0]["email"] = "123@.com"
        cls.data_email[4][0]["email"] = "123@naver."
        cls.data_email[6][0]["email"] = "@naver.com"

        cls.data_password = defaultdict(
            lambda: [
                {
                    "username": "zxKing_@",
                    "email": "uoip@gmail.com",
                },
                400,
            ]
        )
        cls.data_password[0]
        cls.data_password[1][0]["password2"] = "123asd!!"
        # cls.data_password[1][1]["password"]="123asd!!"

        cls.data_password[2][0]["password2"] = "123asd!!`|"
        cls.data_password[2][0]["password"] = "123asd!!`|"

        cls.data_password[3][0]["password2"] = "123asd!!"
        cls.data_password[3][0]["password"] = "123ssd!!"

        cls.data_password[4][0]["password2"] = "123asdaa"
        cls.data_password[4][0]["password"] = "123asdaa"

        cls.data_password[5][0]["password2"] = "aaaasd!!"
        cls.data_password[5][0]["password"] = "aaaasd!!"

        cls.data_password[6][0]["password2"] = "123123!!"
        cls.data_password[6][0]["password"] = "123123!!"

        cls.data_password[6][0]["password2"] = "123a!!"
        cls.data_password[6][0]["password"] = "123a!!"

        cls.data_password[6][0]["password2"] = "123123!!"
        cls.data_password[6][0]["password"] = "123123!!"

    def test_normal(self):
        url = reverse("signup/out")
        data = {
            "username": "zxcvbnasdf_-",
            "email": "abcd@naver.com",
            "password": "asdf1234!!",
            "password2": "asdf1234!!",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)

    def test_wrong_username(self):
        url = reverse("signup/out")
        for _, data in self.data_username.items():
            response = self.client.post(url, data[0])
            self.assertEqual(response.status_code, data[1])

    def test_wrong_email(self):
        url = reverse("signup/out")
        for _, data in self.data_email.items():
            response = self.client.post(url, data[0])
            self.assertEqual(response.status_code, data[1])

    def test_wrong_password(self):
        url = reverse("signup/out")
        for _, data in self.data_password.items():
            response = self.client.post(url, data[0])
            self.assertEqual(response.status_code, data[1])


# Create your tests here.
