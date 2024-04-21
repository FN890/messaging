from rest_framework.test import APIRequestFactory
from django.test import TestCase
from messaging.app.views import PostMessage, GetNewMessages, GetMessagesByIndices, DeleteMessages
from messaging.app.models import Message
from django.urls import reverse
from django.core.management import call_command


class MessagesTest(TestCase):

    fixture_path = "messaging/app/fixtures/example_data.json"

    def setUp(self):
        self.factory = APIRequestFactory()
        self.get_view_new_messages = GetNewMessages.as_view()
        self.get_view_messages_by_indices = GetMessagesByIndices.as_view()
        self.post_view_message = PostMessage.as_view()
        self.delete_view_message = DeleteMessages.as_view()
        call_command("loaddata", self.fixture_path, verbosity=0)

    def tearDown(self):
        call_command("flush", verbosity=0, interactive=False)

    def test_new_messages_when_no_messages_should_404(self):
        self.tearDown()
        test_user_id = 1
        test_last_update = "2000-01-01T12:00:00+02:00"
        url = reverse("get-messages-last-update",
                      kwargs={"user_id": test_user_id, "last_update": test_last_update})
        get_request = self.factory.get(url)
        response = self.get_view_new_messages(
            get_request, user_id=test_user_id, last_update=test_last_update)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, {"error": "No messages found."})

    def test_new_messages_when_future_date_should_404(self):
        test_user_id = 1
        test_last_update = "9999-01-01T12:00:00+02:00"
        url = reverse("get-messages-last-update",
                      kwargs={"user_id": test_user_id, "last_update": test_last_update})
        get_request = self.factory.get(url)
        response = self.get_view_new_messages(
            get_request, user_id=test_user_id, last_update=test_last_update)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, {"error": "No messages found."})

    def test_new_messages_when_very_old_date_should_200_with_all_messages(self):
        test_user_id = 1
        test_last_update = "1900-01-01T12:00:00+02:00"
        url = reverse("get-messages-last-update",
                      kwargs={"user_id": test_user_id, "last_update": test_last_update})
        get_request = self.factory.get(url)
        response = self.get_view_new_messages(
            get_request, user_id=test_user_id, last_update=test_last_update)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 5)

    def test_new_messages_when_messages_exist_should_200_with_only_new_messages(self):
        test_user_id = 1
        test_last_update = "2500-01-04T12:10:00+02:00"
        url = reverse("get-messages-last-update",
                      kwargs={"user_id": test_user_id, "last_update": test_last_update})
        get_request = self.factory.get(url)
        response = self.get_view_new_messages(
            get_request, user_id=test_user_id, last_update=test_last_update)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_messages_by_indices_when_no_message_should_404(self):
        self.tearDown()
        test_user_id = 1
        test_start_index = 0
        test_end_index = 1
        url = reverse("get-messages-indices",
                      kwargs={"user_id": test_user_id, "start_index": test_start_index, "end_index": test_end_index})
        get_request = self.factory.get(url)
        response = self.get_view_messages_by_indices(
            get_request, user_id=test_user_id, start_index=test_start_index, end_index=test_end_index)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, {"error": "No messages found."})

    def test_messages_by_indices_when_start_index_greater_than_end_index_should_404(self):
        test_user_id = 1
        test_start_index = 99
        test_end_index = 0
        url = reverse("get-messages-indices",
                      kwargs={"user_id": test_user_id, "start_index": test_start_index, "end_index": test_end_index})
        get_request = self.factory.get(url)
        response = self.get_view_messages_by_indices(
            get_request, user_id=test_user_id, start_index=test_start_index, end_index=test_end_index)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, {"error": "No messages found."})

    def test_messages_by_indices_when_large_end_index_should_200_with_all_messages(self):
        test_user_id = 1
        test_start_index = 0
        test_end_index = 99
        url = reverse("get-messages-indices",
                      kwargs={"user_id": test_user_id, "start_index": test_start_index, "end_index": test_end_index})
        get_request = self.factory.get(url)
        response = self.get_view_messages_by_indices(
            get_request, user_id=test_user_id, start_index=test_start_index, end_index=test_end_index)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 5)

    def test_messages_by_indices_should_200_with_correct_size(self):
        test_user_id = 1
        test_start_index = 0
        test_end_index = 3
        url = reverse("get-messages-indices",
                      kwargs={"user_id": test_user_id, "start_index": test_start_index, "end_index": test_end_index})
        get_request = self.factory.get(url)
        response = self.get_view_messages_by_indices(
            get_request, user_id=test_user_id, start_index=test_start_index, end_index=test_end_index)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

    def test_send_message_with_valid_data_should_201(self):
        url = reverse("post-message")
        post_request = self.factory.post(
            url, {"recipient": 1, "sender": 2, "message": "This is a message"})
        response = self.post_view_message(post_request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["message"], "This is a message")

    def test_send_message_with_invalid_recipient_should_400(self):
        url = reverse("post-message")
        post_request = self.factory.post(
            url, {"recipient": 99, "sender": 2, "message": "This is a message"})
        response = self.post_view_message(post_request)

        self.assertEqual(response.status_code, 400)
        self.assertIn("object does not exist", str(
            response.data["recipient"][0]))

    def test_send_message_with_invalid_sender_should_400(self):
        url = reverse("post-message")
        post_request = self.factory.post(
            url, {"recipient": 1, "sender": 99, "message": "This is a message"})
        response = self.post_view_message(post_request)

        self.assertEqual(response.status_code, 400)
        self.assertIn("object does not exist", str(response.data["sender"][0]))

    def test_send_message_with_no_message_should_400(self):
        url = reverse("post-message")
        post_request = self.factory.post(
            url, {"recipient": 1, "sender": 2})
        response = self.post_view_message(post_request)

        self.assertEqual(response.status_code, 400)
        self.assertIn("This field is required",
                      str(response.data["message"][0]))

    def test_delete_message_should_204(self):
        self.assertTrue(Message.objects.filter(pk=1).exists(), "Should exist.")

        url = reverse("delete-messages") + "?message_ids=1"
        delete_request = self.factory.delete(url)
        response = self.delete_view_message(delete_request)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data, {"success": "Message(s) deleted."})
        self.assertFalse(Message.objects.filter(
            pk=1).exists(), "Should not exist.")

    def test_delete_messages_should_204(self):
        self.assertTrue(Message.objects.filter(pk=1).exists(), "Should exist.")
        self.assertTrue(Message.objects.filter(pk=2).exists(), "Should exist.")

        url = reverse("delete-messages") + "?message_ids=1&message_ids=2"
        delete_request = self.factory.delete(url)
        response = self.delete_view_message(delete_request)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data, {"success": "Message(s) deleted."})
        self.assertFalse(Message.objects.filter(
            pk=1).exists(), "Should not exist.")
        self.assertFalse(Message.objects.filter(
            pk=2).exists(), "Should not exist.")

    def test_delete_message_no_id_should_204(self):
        url = reverse("delete-messages")
        delete_request = self.factory.delete(url)
        response = self.delete_view_message(delete_request)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {"error": "No message IDs provided."})

    def test_delete_message_invalid_id_should_404(self):
        url = reverse("delete-messages") + "?message_ids=99"
        delete_request = self.factory.delete(url)
        response = self.delete_view_message(delete_request)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, {"error": "Message(s) not found."})

    def test_delete_message_with_valid_and_invalid_ids_should_204(self):
        self.assertTrue(Message.objects.filter(pk=1).exists(), "Should exist.")

        url = reverse("delete-messages") + "?message_ids=99&message_ids=1"
        delete_request = self.factory.delete(url)
        response = self.delete_view_message(delete_request)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data, {"success": "Message(s) deleted."})
        self.assertFalse(Message.objects.filter(
            pk=1).exists(), "Should not exist.")
