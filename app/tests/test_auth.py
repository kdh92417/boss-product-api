
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from app.models import User


class AuthTests(APITestCase):
    def setUp(self):
        pass

    def test_success_email_signup_api(self):
        signup_data = {
            "phone_number": "010-2312-2122",
            "password": "password"
        }

        signup_response = self.client.post(reverse("signup"), HTTP_ACCEPT="application/json", format="json", data=signup_data)

        self.assertEqual(status.HTTP_201_CREATED, signup_response.status_code)
        signup_user = User.objects.filter(phone_number=signup_data["phone_number"]).first()
        self.assertIsNotNone(signup_user)


