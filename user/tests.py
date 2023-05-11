from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from collections import defaultdict
from user.models import User


# Create your tests here.
class UserBaseTestCase(APITestCase):
    """
    회원가입과 로그인이 필요한 기능들을 위한 부모 클래스입니다.
    """

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


class UserSignOutTestCase(UserBaseTestCase):
    """
    탈퇴기능을 검정하기 위한 케이스
    """

    def test_logined(self):
        """
        정상 케이스
        """
        url = reverse("signup/out")
        response = self.client.put(
            path=url,
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
            data=self.user_data,
        )
        self.assertEqual(response.status_code, 200)

    def test_annon(self):
        """
        비 로그인 회원
        """
        url = reverse("signup/out")
        response = self.client.put(
            path=url,
            data=self.user_data,
        )
        self.assertEqual(response.status_code, 401)

    def test_wrong_password(self):
        """
        비밀번호 불일치
        """
        url = reverse("signup/out")
        response = self.client.put(
            path=url,
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
            data={"password": "asdf!!1234"},
        )
        self.assertEqual(response.status_code, 400)

    def test_wrong_token(self):
        """
        토큰 유효하지 않음
        """
        url = reverse("signup/out")
        response = self.client.put(
            path=url,
            HTTP_AUTHORIZATION=f"Bearer {self.access[:-3]}123",
            data=self.user_data,
        )
        self.assertEqual(response.status_code, 401)


class UserPATCHTestCase(UserBaseTestCase):
    """
    유저정보 수정을 검증하기 위한 클래스
    """

    @classmethod
    def setUpTestData(cls) -> None:
        """
        부모클래스에서 사용한 user 정보는 탈퇴 검증과정에서 is_activate가 비활성화되므로 새로 지정한다.
        """
        cls.user = User.objects.create_user(
            username="zxcvbnasdf_@",
            email="abcd@navers.com",
            password="asdf1234!!",
        )
        cls.user_data = {"username": "zxcvbnasdf_@", "password": "asdf1234!!"}

    def setUp(self) -> None:
        self.access = self.client.post(reverse("token"), self.user_data).data["access"]

    def test_logined(self):
        """
        일반적으로 로그인한 유저의 경우
        """

        # 비밀번호 변경
        url = reverse("signup/out")
        data = {
            "current_password": "asdf1234!!",
            "password": "asdf1234!!",
            "password2": "asdf1234!!",
        }
        response = self.client.patch(
            path=url, HTTP_AUTHORIZATION=f"Bearer {self.access}", data=data
        )
        self.assertEqual(response.status_code, 200)

        # 아무것도 변경안함
        data = {
            "current_password": "asdf1234!!",
        }
        response = self.client.patch(
            path=url, HTTP_AUTHORIZATION=f"Bearer {self.access}", data=data
        )
        self.assertEqual(response.status_code, 200)

        # 비밀번호 변경 시도 - 하나만 입력
        data = {"current_password": "asdf1234!!", "password2": "asdf1234!!"}
        response = self.client.patch(
            path=url, HTTP_AUTHORIZATION=f"Bearer {self.access}", data=data
        )
        self.assertEqual(response.status_code, 400)

        # 비밀 번호 불일치
        data = {
            "current_password": "asdf1234!!",
            "password": "asdf123!!",
            "password2": "asdf1234!!",
        }
        response = self.client.patch(
            path=url, HTTP_AUTHORIZATION=f"Bearer {self.access}", data=data
        )
        self.assertEqual(response.status_code, 400)

    def test_annon(self):
        """
        비 로그인 익명 사용자가 시도시
        """
        url = reverse("signup/out")
        data = {
            "current_password": "asdf1234!!",
            "password": "asdf1234!!",
            "password2": "asdf1234!!",
        }
        response = self.client.patch(path=url, data=data)
        self.assertEqual(response.status_code, 401)

    def test_wrong_token(self):
        """
        유효하지 않은 토큰
        """

        url = reverse("signup/out")
        data = {
            "current_password": "asdf1234!!",
            "password": "asdf1234!!",
            "password2": "asdf1234!!",
        }
        response = self.client.patch(
            path=url,
            data=data,
            HTTP_AUTHORIZATION=f"Bearer {self.access[:-3]}123",
        )
        self.assertEqual(response.status_code, 401)

    def test_wrong_password(self):
        url = reverse("signup/out")
        data = {
            "current_password": "asdf11234!!",
            "password": "asdf1234!!",
            "password2": "asdf1234!!",
        }
        response = self.client.patch(
            path=url,
            data=data,
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
        )
        self.assertEqual(response.status_code, 400)


class UserGetTestCase(UserBaseTestCase):
    def test_get_logined(self):
        url = reverse("signup/out")
        response = self.client.get(path=url, HTTP_AUTHORIZATION=f"Bearer {self.access}")
        self.assertEqual(response.status_code, 200)

    def test_get_annon(self):
        url = reverse("signup/out")
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, 401)

    def test_wrong_token(self):
        url = reverse("signup/out")
        response = self.client.put(
            path=url,
            HTTP_AUTHORIZATION=f"Bearer {self.access[:-3]}123",
        )
        self.assertEqual(response.status_code, 401)
