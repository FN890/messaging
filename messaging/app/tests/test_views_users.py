from rest_framework.test import APIRequestFactory
from django.test import TestCase
from messaging.app.views import GetUsers, PostUser, DeleteUser
from messaging.app.serializers import CustomUserSerializer
from messaging.app.models import CustomUser
from django.urls import reverse


class UsersTest(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.get_view = GetUsers.as_view()
        self.post_view = PostUser.as_view()
        self.delete_view = DeleteUser.as_view()
        self.get_url = reverse("get-users")
        self.post_url = reverse("post-users")

    def test_get_when_no_users_should_404(self):
        get_request = self.factory.get(self.get_url)
        response = self.get_view(get_request)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, {"error": "No users found."})

    def test_get_when_users_should_200(self):
        post_request = self.factory.post(self.post_url, {"username": "unique_name"})
        self.post_view(post_request)

        get_request = self.factory.get(self.get_url)
        response = self.get_view(get_request)
        expected_data = CustomUserSerializer(
            CustomUser.objects.all(), many=True).data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_data)

    def test_add_user_unique_name_should_201(self):
        post_request = self.factory.post(self.post_url, {"username": "unique_name"})
        response = self.post_view(post_request)

        self.assertEqual(response.status_code, 201)
        self.assertIn("unique_name", response.data["username"])

    def test_add_user_not_unique_name_should_400(self):
        post_request = self.factory.post(
            self.post_url, {"username": "unique_name"})
        second_post_request = self.factory.post(
            self.post_url, {"username": "unique_name"})

        self.post_view(post_request)
        response = self.post_view(second_post_request)

        self.assertEqual(response.status_code, 400)

    def test_delete_existing_user_should_204(self):
        delete_url = reverse("delete-users") + "?user_id=1"
        post_request = self.factory.post(
            self.post_url, {"username": "unique_name"})
        delete_request = self.factory.delete(delete_url)

        self.post_view(post_request)
        response = self.delete_view(delete_request)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data, {"success": "User deleted."})

    def test_delete_no_user_should_400(self):
        url = reverse("delete-users")
        delete_request = self.factory.delete(url)

        response = self.delete_view(delete_request)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {"error": "No user ID provided."})

    def test_delete_invalid_user_should_404(self):
        url = reverse("delete-users") + "?user_id=100"
        delete_request = self.factory.delete(url)
        response = self.delete_view(delete_request)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, {"error": "User not found."})
