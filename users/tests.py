from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient


class UserAuthenticationTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = get_user_model().objects.create_user(
            username="JohnDoe", password="secret"
        )

    def test_can_sign_up(self) -> None:
        client = APIClient()
        response = client.post(
            "/api/v1/dj-rest-auth/registration/",
            data={
                "username": "JaneDoe",
                "password1": "f00B@rb@2",
                "password2": "f00B@rb@2",
            },
        )

        self.assertEqual(response.status_code, 204)
        users = get_user_model().objects.filter(username="JohnDoe")
        self.assertEqual(len(users), 1)

    def test_can_sign_in(self) -> None:
        client = APIClient()
        response = client.post(
            "/api/v1/dj-rest-auth/login/",
            data={
                "username": "JohnDoe",
                "password": "secret",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data["key"])

    def test_can_show_user(self) -> None:
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.get("/api/v1/dj-rest-auth/user/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["username"], "JohnDoe")

    def test_can_sign_out(self) -> None:
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.post("/api/v1/dj-rest-auth/logout/")

        self.assertEqual(response.status_code, 200)

    def test_can_update_profile(self) -> None:
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.put(
            "/api/v1/dj-rest-auth/user/",
            data={
                "username": "JohnDoe123",
                "first_name": "John",
                "last_name": "Doe",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["username"], "JohnDoe123")
        self.assertEqual(response.data["first_name"], "John")
        self.assertEqual(response.data["last_name"], "Doe")

        user = get_user_model().objects.get(pk=self.user.id)
        self.assertEqual(user.username, "JohnDoe123")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")

    def test_can_update_password(self) -> None:
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.post(
            "/api/v1/dj-rest-auth/password/change/",
            data={
                "new_password1": "f00b@rB@Z",
                "new_password2": "f00b@rB@Z",
            },
        )

        self.assertEqual(response.status_code, 200)
