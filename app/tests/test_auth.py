from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from app.models import User
from app.tests.helper import create_fake_user


class AuthTests(APITestCase):
    def setUp(self):
        pass

    def test_success_email_signup_api(self):
        signup_data = {"phone_number": "010-2312-2122", "password": "password"}

        signup_response = self.client.post(
            reverse("signup"),
            HTTP_ACCEPT="application/json",
            format="json",
            data=signup_data,
        )

        self.assertEqual(status.HTTP_201_CREATED, signup_response.status_code)
        signup_user = User.objects.filter(
            phone_number=signup_data["phone_number"]
        ).first()
        self.assertIsNotNone(signup_user)

    def test_fail_signup_bad_phone_number_format(self):
        signup_data = {"phone_number": "010-2312--2122afafas", "password": "password"}

        signup_response = self.client.post(
            reverse("signup"),
            HTTP_ACCEPT="application/json",
            format="json",
            data=signup_data,
        )

        self.assertEqual(status.HTTP_400_BAD_REQUEST, signup_response.status_code)

    def test_success_login(self):
        user, password = create_fake_user()

        login_data = {"password": password, "phone_number": user.phone_number}

        login_response = self.client.post(
            reverse("login"),
            HTTP_ACCEPT="application/json",
            format="json",
            data=login_data,
        )
        self.assertEqual(status.HTTP_200_OK, login_response.status_code)

        login_response_json = login_response.json()
        login_response_json_data = login_response_json["data"]

        self.assertIsNotNone(login_response_json_data)
        self.assertIsNotNone(login_response_json_data["access_token"])
        self.assertIsNotNone(login_response_json_data["refresh_token"])
