from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class AuthTestCase(APITestCase):
    username = "testuser"
    password = "StrongPassword123"

    def test_user_registration(self):
        url = "/api/auth/register/"
        data = {
            "username": self.username,
            "password": self.password,
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username=self.username).exists())

    def test_login_returns_tokens(self):
        User.objects.create_user(
            username=self.username,
            password=self.password,
        )

        url = "/api/auth/login/"
        data = {
            "username": self.username,
            "password": self.password,
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_protected_endpoint_requires_auth(self):
        response = self.client.get("/api/v1/projects/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_access_with_valid_token(self):
        User.objects.create_user(
            username=self.username,
            password=self.password,
        )

        login_response = self.client.post(
            "/api/auth/login/",
            {
                "username": self.username,
                "password": self.password,
            },
        )

        access = login_response.data["access"]

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {access}",
        )

        response = self.client.get("/api/v1/projects/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
