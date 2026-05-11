from rest_framework import status
from rest_framework.test import APITestCase

from .models import Entry, User


class GuestBookAPITest(APITestCase):

    def test_create_entry(self):
        payload = {
            "name": "Muberra",
            "subject": "Hello",
            "message": "First message",
        }

        response = self.client.post(
            "/api/entries/create/",
            payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Entry.objects.count(), 1)

    def test_get_entries(self):
        user = User.objects.create(name="Muberra")

        Entry.objects.create(
            user=user,
            subject="Test Subject",
            message="Test Message",
        )

        response = self.client.get("/api/entries/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["entries"]), 1)

    def test_get_users(self):
        user = User.objects.create(name="Muberra")

        Entry.objects.create(
            user=user,
            subject="Last Subject",
            message="Last Message",
        )

        response = self.client.get("/api/users/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["users"]), 1)

        self.assertEqual(
            response.data["users"][0]["last_entry"],
            "Last Subject | Last Message",
        )

    def test_model_string_representations(self):
        user = User.objects.create(name="Muberra")

        entry = Entry.objects.create(
            user=user,
            subject="Test Subject",
            message="Test Message",
        )

        self.assertEqual(str(user), "Muberra")
        self.assertEqual(str(entry), "Test Subject")


from rest_framework import status
from rest_framework.test import APITestCase

from .models import Entry, User


class GuestBookIntegrationTest(APITestCase):

    def test_guestbook_full_integration_flow(self):
        payloads = [
            {"name": "user_1", "subject": "Subject 1", "message": "Message 1"},
            {"name": "user_2", "subject": "Subject 2", "message": "Message 2"},
            {"name": "user_3", "subject": "Subject 3", "message": "Message 3"},
            {"name": "user_1", "subject": "Subject 4", "message": "Message 4"},
            {"name": "user_2", "subject": "Subject 5", "message": "Message 5"},
            {"name": "user_3", "subject": "Subject 6", "message": "Message 6"},
            {"name": "user_1", "subject": "Subject 7", "message": "Message 7"},
            {"name": "user_2", "subject": "Subject 8", "message": "Message 8"},
        ]

        for payload in payloads:
            response = self.client.post(
                "/api/entries/create/",
                payload,
                format="json",
            )
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(Entry.objects.count(), 8)

        invalid_payload = {
            "name": "   ",
            "subject": "Invalid Subject",
            "message": "Invalid Message",
        }

        validation_response = self.client.post(
            "/api/entries/create/",
            invalid_payload,
            format="json",
        )

        self.assertEqual(validation_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", validation_response.data)

        first_page_response = self.client.get("/api/entries/")
        second_page_response = self.client.get("/api/entries/?page=2")
        third_page_response = self.client.get("/api/entries/?page=3")

        self.assertEqual(first_page_response.status_code, status.HTTP_200_OK)
        self.assertEqual(first_page_response.data["count"], 8)
        self.assertEqual(first_page_response.data["page_size"], 3)
        self.assertEqual(first_page_response.data["total_pages"], 3)
        self.assertEqual(first_page_response.data["current_page_number"], 1)
        self.assertEqual(len(first_page_response.data["entries"]), 3)
        self.assertIsNotNone(first_page_response.data["links"]["next"])
        self.assertIsNone(first_page_response.data["links"]["previous"])

        self.assertEqual(second_page_response.status_code, status.HTTP_200_OK)
        self.assertEqual(second_page_response.data["current_page_number"], 2)
        self.assertEqual(len(second_page_response.data["entries"]), 3)
        self.assertIsNotNone(second_page_response.data["links"]["next"])
        self.assertIsNotNone(second_page_response.data["links"]["previous"])

        self.assertEqual(third_page_response.status_code, status.HTTP_200_OK)
        self.assertEqual(third_page_response.data["current_page_number"], 3)
        self.assertEqual(len(third_page_response.data["entries"]), 2)
        self.assertIsNone(third_page_response.data["links"]["next"])
        self.assertIsNotNone(third_page_response.data["links"]["previous"])

        first_entry = first_page_response.data["entries"][0]

        self.assertEqual(first_entry["user"], "user_2")
        self.assertEqual(first_entry["subject"], "Subject 8")
        self.assertEqual(first_entry["message"], "Message 8")

        users_response = self.client.get("/api/users/")

        self.assertEqual(users_response.status_code, status.HTTP_200_OK)
        self.assertNotIn("count", users_response.data)
        self.assertNotIn("page_size", users_response.data)
        self.assertNotIn("total_pages", users_response.data)
        self.assertNotIn("links", users_response.data)

        users_data = {user["username"]: user for user in users_response.data["users"]}

        self.assertEqual(len(users_data), 3)

        self.assertEqual(users_data["user_1"]["total_messages"], 3)
        self.assertEqual(users_data["user_1"]["last_entry"], "Subject 7 | Message 7")

        self.assertEqual(users_data["user_2"]["total_messages"], 3)
        self.assertEqual(users_data["user_2"]["last_entry"], "Subject 8 | Message 8")

        self.assertEqual(users_data["user_3"]["total_messages"], 2)
        self.assertEqual(users_data["user_3"]["last_entry"], "Subject 6 | Message 6")

    def test_model_string_representations(self):
        user = User.objects.create(name="Muberra")

        entry = Entry.objects.create(
            user=user,
            subject="Test Subject",
            message="Test Message",
        )

        self.assertEqual(str(user), "Muberra")
        self.assertEqual(str(entry), "Test Subject")
