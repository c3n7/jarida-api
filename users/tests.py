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

    # def test_can_sign_out(self) -> None:
    #     client = APIClient()
    #     response = client.post(
    #         "/api/v1/dj-rest-auth/login/",
    #         data={
    #             "username": "JohnDoe",
    #             "password": "secret",
    #         },
    #     )

    #     print(self.client)
    #     response = client.post(
    #         "/api/v1/dj-rest-auth/logout/",
    #     )

    #     self.assertEqual(response.status_code, 200)
    #     # self.assertIsNotNone(response.data["key"])

    #     response = client.post(
    #         "/api/v1/dj-rest-auth/logout/",
    #     )
    #     # print(response.request.user)
